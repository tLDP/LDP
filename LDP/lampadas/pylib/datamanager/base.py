#!/usr/bin/python

"""
This module implements the base classes upon which all the individual
data managers are built.
"""

from Globals import *
from BaseClasses import LampadasCollection
from Database import db
from cache import Cache, CACHE_UNLIMITED
import string

# FIXME: use sqlgen ?

class UnknownField(Exception) :
    """
    Exception raised when unknown field is used with TableField.
    """

class UnknownFieldType(Exception) :
    """
    Exception raised when unknown type is used with TableField.
    """

class UnknownOperator(Exception):
    """
    Exception if a filter has an unrecognized operator.
    """
    
class TableField:
    """
    This class defines a field in a database table, i.e., a column.
    """

    def __init__(self, table):
        self.table = table

    def get_default(self):
        if self.data_type in ('sequence', 'int', 'float'): return 0
        elif self.data_type in ('string', ''): return ''
        elif self.data_type=='list':           return []
        elif self.data_type=='time':           return ''
        elif self.data_type=='date':           return ''
        elif self.data_type=='bool':           return 0
        elif self.data_type=='created':        return now_string()
        elif self.data_type=='updated':        return now_string()
        elif self.data_type=='creator':
            if state.user:
                return state.user.username
            else:
                return ''
        elif self.data_type=='updater':
            if state.user:
                return state.user.username
            else:
                return ''
        else:
            raise UnknownFieldType('Unrecognized type: %s'%self.data_type)
        
    def field_to_attr(self, value):
        if self.data_type in ('sequence', 'int', 'float'):
            return safeint(value)
        elif self.data_type in ('string', ''): return trim(value)
        elif self.data_type=='list':           return trim(value).split()
        elif self.data_type=='time':           return time2str(value)
        elif self.data_type=='date':           return date2str(value)
        elif self.data_type=='bool':           return tf2bool(value)
        elif self.data_type=='created':        return time2str(value)
        elif self.data_type=='updated':        return time2str(value)
        elif self.data_type=='creator':        return trim(value)
        elif self.data_type=='updater':        return trim(value)
        else:
            raise UnknownFieldType('Unrecognized type: %s'%self.data_type)

    def attr_to_field(self, value):
        global current_session
        if self.data_type in ('sequence', 'int', 'float'):
            if self.nullable==1 and value==0:
                return 'NULL'
            else:
                return str(value)
        elif self.data_type=='string':  return wsq(str(value))
        elif self.data_type=='list':    return wsq(string.join(value))
        elif self.data_type=='bool':    return wsq(bool2tf(value))
        elif self.data_type=='date':    return wsq(str(value))
        elif self.data_type=='time':    return wsq(str(value))
        elif self.data_type=='created': return wsq(str(value))
        elif self.data_type=='updated': return wsq(now_string())
        elif self.data_type=='creator': return wsq(value)
        elif self.data_type=='updater':
            if current_session:
                return wsq(current_session.user.username)
            else:
                return wsq('')
        else :
            raise UnknownFieldType('Unrecognized data type definition '
                                   'data= %s invalid type=%s' 
                                   % (key,self.data_type))

class TableFields(LampadasCollection):

    def find_attribute(self, attribute):
        for key in self.keys():
            field = self[key]
            if field.attribute==attribute:
                return field

class DataTable(LampadasCollection):
    """
    This class defines a table in the RDBMS back end.
    """

    def __init__(self, table_name, field_dictionary):
        LampadasCollection.__init__(self)
        self.name   = table_name
        self.fields = TableFields()
        
        self.key_list   = []
        self.field_list = []
        for field_name in field_dictionary.keys():
            field = field_dictionary[field_name]
            data_field = TableField(self)
            data_field.table_name   = self.name
            data_field.index        = len(self.fields)
            data_field.field_name   = field_name
            data_field.key_field    = field['key_field']
            data_field.data_type    = field['data_type']
            data_field.nullable     = field['nullable']
            data_field.i18n         = field['i18n']
            data_field.foreign_key  = field['foreign_key']
            if field.has_key('foreign_attr'):
                data_field.foreign_attr = field['foreign_attr']
            else:
                data_field.foreign_attr = ''
            if field.has_key('attribute'):
                data_field.attribute = field['attribute']
            else:
                data_field.attribute = data_field.field_name

            # Load the default value AFTER populating the other fields.
            if field.has_key('default'):
                data_field.default = field['default']
            else:
                data_field.default = data_field.get_default()
            self.fields[field_name] = data_field
            self.field_list.append(field_name)
            if data_field.key_field==1:
                self.key_list.append(data_field.field_name)
        self.select   = 'SELECT %s FROM %s' % (string.join(self.field_list, ', '), self.name)

    def id_field(self):
        return self.fields[self.key_list[0]]

    def load_row(self, object, row):
        for key in self.field_list:
            field = self.fields[key]
            value = field.field_to_attr(row[field.index])
            setattr(object, field.attribute, value)
        object.in_database = 1
        object.changed = 0
        object.key = self.get_key(object)

    def get_row_key(self, row):
        if len(self.key_list) > 1:
            newkey = ''
        for key in self.field_list:
            field = self.fields[key]
            if field.key_field==1:
                value = field.field_to_attr(row[field.index])
                if len(self.key_list)==1:
                    newkey = value
                else:
                    newkey = trim(newkey + ' ' + str(value))
        return newkey

    def get_key(self, object):
        if len(self.key_list) > 1:
            newkey = ''
        for key in self.field_list:
            field = self.fields[key]
            if field.key_field==1:
                value = getattr(object, field.attribute)
                if len(self.key_list)==1:
                    newkey = value
                else:
                    newkey = trim(newkey + ' ' + str(value))
        return newkey

class DataManager(DataTable):
    """
    This class provides high level access to a database table.
    
    It loads and saves data from the table into an object or a DataSet,
    or a subclass thereof. The class of objects and data sets that
    are returned can be set using the set_object() and set_dataset()
    functions.
    
    You can request a single object (row), or you can specify a set of criteria,
    which are then translated into a WHERE clause.
    """

    def __init__(self, table_name, field_dictionary):
        DataTable.__init__(self, table_name, field_dictionary)
        self.table   = DataTable(table_name, field_dictionary)
        self.reset_cache()

    def reset_cache(self):
        """
        Initialize this data manager's object cache.

        Any contents in the cache are discarded.
        """
        self.cache        = Cache()
        self.all_cached   = 0
        self.last_synched = ''
    
    def preload(self):
        """
        Handles a client request to preload all objects from the database,
        fully populating the local cache and preparing for subsequent
        client requests.

        Preloading can result in significant performance benefits,
        because data managers who have preloaded their cache can
        fill more client requests from cache, avoiding expensive
        database accesses.

        Not all requests for preloading are honored. To be preloaded,
        a datamanager's cache size must be set to CACHE_UNLIMITED.
        Also, only one call is honored. Subsequent calls are
        silently ignored. This makes it safe and efficient for
        clients to request preloading, without needing to know
        whether or not the data manager has already been preloaded.
        """
        if self.all_cached==1:
            return

        # FIXME: Also try to preload caches that are not unlimited,
        # but are large enough to hold all existing objects.
        # Use a SQL COUNT(*) function to make this determination,
        # so we don't waste lots of time attempting to preload
        # a cache that cannot be preloaded.
        if self.cache.size <> CACHE_UNLIMITED:
            return
        #print 'Preloading ' + self.table.name
        self.get_all()
        #i18n_table = self.table.name + '_i18n'
        #if self.dms.has_key(i18n_table):
        #    i18n_dm = self.dms[i18n_table]
        #    i18n_dm.preload()
        
    def get_by_id(self, id):
        """
        Returns an individual object whose primary key field matches
        the specified id.

        If the object is in the cache, the cached object is returned.
        Objects which have more than one primary key field cannot be
        reliably retrieved using this function. In this event, only the
        first matching object will be returned.
        """
        
        object = self.cache.get_by_key(id)
        if object==None:
            data_field = self.table.id_field()
            sql = self.table.select + ' WHERE ' + data_field.field_name + '=' + data_field.attr_to_field(id)
            cursor = db.select(sql)
            row = cursor.fetchone()
            if row==None: return
            object = self.row_to_object(row)
        return object

    def get_by_keys(self, filters):
        """
        Returns all objects which match the supplied filters.
        """
        if self.cache.filled==1:
            self.all_cached = 0
        if self.all_cached==1:
            return self.get_cached_by_keys(filters)
        else:
            sql = self.filters_to_sql(filters)
            return self.get_sql(sql)

    def get_cached_by_keys(self, filters):
        """
        This private function fills keyed requests directly from the
        object cache.
        
        No checking is performed to determine whether the cache contains
        all objects which fit the request. Therefore, this function
        should only be called by data managers whose caches are preloaded.
        See the preload() function for more information on preloading.
        """
        sql = self.filters_to_sql(filters)
        function_text = self.filters_to_function(filters)
        print 'Function text: '
        print function_text
        code = compile(function_text, '<string>', 'exec')
        print 'Code: ' + str(code)
        print 'Code has %s arguments.' % code.co_argcount

        self.test_object_filters.im_func.func_code = code
        #print 'Method code: ' + str(self.test_object_filters.im_func.func_code)
        good_keys = filter(self.test_object_filters, self.cache.keys())
        print 'Good keys: ' + str(good_keys)
        dataset = self.new_dataset()
        for key in good_keys:
            dataset[key] = self.cache[key]
        return dataset

    def test_object_filters(self, key):
        return 1
    
    def filters_to_function(self, filters):
        """
        Converts a list of filters into a Python function which tests
        an object to see if it matches the filters.

        Precompiling filter tests speeds up key filtering enormously.
        
        The generated function accepts a single parameter, "key".
        It retrieves the object with that key in the object
        cache and tests for a match. If the object matches all
        the filters, the generated function returns 1.
        Otherwise, it returns 0.
        """
        code = WOStringIO()
        code.write('def test_cached_object(key):\n')
        code.write('    object = self.cache[key]\n')
        for filter in filters:
            attribute, operator, value = filter
            test_value = repr(value)
            code.write('    obj_value = object.%s\n' % (attribute))
            if operator.upper()=='LIKE':
                code.write('    if %s > len(%s): return 0\n' % (len(value), obj_value))
                code.write('    return (%s <> obj_value.upper()[:%s])\n' % (test_value.upper(), len(value)))
            elif operator in ['<>', '<', '<=', '=', '>=', '>']:
                if operator=='=':
                    operator = '=='
                code.write('    return (object.%s %s %s)\n' % (attribute, operator, repr(value)))
            else:
                raise UnknownOperator('Unrecognized operator: %s' % (operator))

        return code.get_value()
            
    def filters_to_sql(self, filters):
        """
        Converts a list of filters into the SQL statement which will
        retrieve matching records from the database.
        """
        wheres = []
        for filter in filters:
            attribute, operator, value = filter
            field = self.table.fields.find_attribute(attribute)
            if operator.upper()=='LIKE':
                wheres.append('upper(' + field_name + ') LIKE ' + field.attr_to_field(value.upper() + '%'))
            else:
                wheres.append(field.field_name + operator + field.attr_to_field(value))
        where = ' WHERE ' + string.join(wheres, ' AND ')
        return self.table.select + where

    def get_all(self):
        """
        Returns a set of all objects managed by this data manager.

        If the data manager's cache proves sufficient to cache all objects,
        the cache will subsequently be considered preloaded, i.e.,
        subsequent calls to get_by_keys() will be served directly from the
        cache, bypassing expensive database accesses. See the preload()
        function for more information on preloading.
        """
        if self.cache.filled==1:
            self.all_cached = 0
        if self.all_cached==0:
            #print 'Loading all of ' + self.table.name + ' into cache.'
            set = self.get_sql(self.table.select)
            if self.cache.filled==0:
                self.all_cached = 1
            return set
        return self.get_cached()

    def synch(self):
        """
        Synchronize objects in the object cache with the database.

        Objects which have been deleted in the database are removed
        from the object cache.
        
        Objects which are out of synch with their database record
        have their attribute set to match the data in the database.
        """
        #print 'Synchronizing ' + self.table.name + ' with database'
        last_synched = self.last_synched        # Remember this, because we're about to overwrite it.
        self.last_synched = now_string()

        # Delete any newly deleted objects.
        sql = 'SELECT identifier FROM deleted WHERE table_name=' + wsq(self.table.name) + ' AND deleted >= ' + wsq(last_synched)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            
            # Load keys for the deleted object
            object = self.new_object()
            if len(self.table.key_list)==1:
                field = self.table.fields[self.table.key_list[0]]
                value = field.field_to_attr(row[0])
                setattr(object, field.attribute, value)
            else:
                values = row[0].split()
                for key in self.table.key_list:
                    field = self.table.fields[key]
                    value = field.field_to_attr(values[field.index])
                    setattr(object, field.attribute, value)
            object.key = self.table.get_key(object)

            #print 'Deleting from ' + self.table.name + ' cache: ' + str(value)
            self.cache.delete(object)

            # FIXME: Delete the object from all data sets which contain it!

        # Update any newly updated objects.
        sql = self.table.select + ' WHERE updated >= ' + wsq(last_synched)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            key = self.table.get_row_key(row)
            if self.cache.has_key(key):
                object = self.cache[key]
                self.table.load_row(object, row)
                #print 'Updating in ' + self.table.name + ' cache: ' + str(object.key)
            else:
                object = self.row_to_object(row)
                self.cache.add(object)
                #print 'Adding in ' + self.table.name + ' cache: ' + str(object.key)

                # FIXME: Add the object to all data sets whose filters it matches.

    def get_cached(self):
        """
        Returns a dataset containing all objects in the object cache.
        """
        #print 'Pulling ' + self.table.name + ' from cache.'
        dataset = self.new_dataset()
        for key in self.cache.keys():
            dataset[key] = self.cache[key]
        return dataset
        
    def get_sql(self, sql):
        """
        Accepts a SQL statement, instantiates the corresponding objects from the
        database, and stores those objects in the data cache if possible.
        """
        #print 'Cache miss, loading: ' + self.table.name
        dataset = self.new_dataset()
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            object = self.row_to_object(row)
            dataset[object.key] = object
            self.cache.add(object)
        return dataset

    def set_object_class(self, object_class):
        self.object_class = object_class
        
    def set_dataset_class(self, dataset_class):
        self.dataset_class = dataset_class

    def new_object(self):
        object = self.object_class(self.dms, self)
        for key in self.table.fields.keys():
            field = self.table.fields[key]
            setattr(object, field.attribute, field.get_default())
        object.changed = 0
        object.in_database = 0
        return object

    def new_dataset(self):
        return self.dataset_class(self)
    
    def row_to_object(self, row):
        object = self.new_object()
        self.table.load_row(object, row)
        return object

    def add(self, object):
        self.save(object)

    def save(self, object):
        object.key = self.table.get_key(object) # New objects need their key calculated.
        if object.changed==0 and object.in_database==0:
            return
        if object.in_database==0:
            field_list = []
            value_list = []
            for key in self.table.field_list:
                field = self.table.fields[key]
                if field.data_type=='created':  # The database is responsible for setting the timestamp.
                    continue
                if field.data_type=='sequence': # When inserting, always increment the value.
                    new_id = db.next_id(self.name, field.field_name)
                    setattr(object, field.attribute, new_id)
                value = field.attr_to_field(getattr(object, field.attribute))
                field_list.append(field.field_name)
                value_list.append(value)
            sql = 'INSERT INTO %s (%s) VALUES (%s)' % (self.table.name, string.join(field_list, ', '), string.join(value_list, ', '))
        else:
            update_list = []
            where_list = []
            for key in self.table.field_list:
                field = self.table.fields[key]
                if field.data_type=='created':
                    continue
                if field.data_type=='updated':
                    value = wsq(now_string())
                else:
                    value = field.attr_to_field(getattr(object, field.attribute))
                update_list.append(field.field_name + '=' + value)
                if field.key_field==1:
                    where_list.append(field.field_name + '=' + value)
            sql = 'UPDATE %s SET %s WHERE %s' % (self.table.name, string.join(update_list, ', '), string.join(where_list, ' AND '))
#            print sql
        db.runsql(sql)
        db.commit()
        self.cache.add(object)
        object.in_database = 1
        object.changed = 0

    def delete(self, object):
        if object.in_database==0:
            return
        self.cache.delete(object)
        wheres = []
        for key in self.table.key_list:
            data_field = self.table.fields[key]
            value = data_field.attr_to_field(getattr(object, data_field.attribute))
            wheres.append(data_field.field_name + '=' + value)
        where = ' WHERE ' + string.join(wheres, ' AND ')
        sql = 'DELETE FROM %s %s' % (self.table.name, where)
        db.runsql(sql)
        db.commit()
        sql = 'INSERT INTO deleted (table_name, identifier) VALUES (%s, %s)' % (wsq(self.table.name), wsq(str(object.key)))
        db.runsql(sql)
        db.commit()

    def delete_by_keys(self, filters):
        dataset = self.get_by_keys(filters)
        for key in dataset.keys():
            object = dataset[key]
            self.delete(object)
    
    def clear(self, dataset):
        for key in dataset.keys():
            self.delete(dataset[key])
