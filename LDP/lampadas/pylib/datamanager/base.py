#!/usr/bin/python

"""
This module implements the base classes upon which all the individual
data managers are built.
"""

from Globals import *
from BaseClasses import LampadasCollection
from Database import db
import string

# FIXME: use sqlgen ?

class UnknownFieldType(Exception) :
    """
    Exception raised when unknown type is used with TableField.
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
        elif self.data_type=='time':           return ''
        elif self.data_type=='date':           return ''
        elif self.data_type=='bool':           return 0
        elif self.data_type=='created':        return now_string()
        elif self.data_type=='updated':        return None
        elif self.data_type=='creator':        return None
        elif self.data_type=='updater':        return None
        else:
            raise UnknownFieldType('Unrecognized type: %s'%self.data_type)
        
    def field_to_attr(self, value):
        if self.data_type in ('sequence', 'int', 'float'):
            return safeint(value)
        elif self.data_type in ('string', ''): return trim(value)
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
        if self.data_type in ('sequence', 'int', 'float'):
            if self.nullable==1 and value==0:
                return 'NULL'
            else:
                return str(value)
        elif self.data_type=='string':  return wsq(str(value))
        elif self.data_type=='bool':    return wsq(bool2tf(value))
        elif self.data_type=='date':    return wsq(str(value))
        elif self.data_type=='time':    return wsq(str(value))
        elif self.data_type=='created': return wsq(str(value))
        elif self.data_type=='updated': return wsq(now_string())
        elif self.data_type=='creator': return wsq(value)
        elif self.data_type=='updater': return wsq(value)
        else :
            raise UnknownFieldType('Unrecognized data type definition '
                                   'data= %s invalid type=%s' 
                                   % (key,self.data_type))

class DataTable(LampadasCollection):
    """
    This class defines a table in the RDBMS back end.
    """

    def __init__(self, table_name, field_dictionary):
        LampadasCollection.__init__(self)
        self.name   = table_name
        self.fields = LampadasCollection()
        
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
        if len(self.key_list) > 1:
            object.key = ''
        for key in self.field_list:
            field = self.fields[key]
            value = field.field_to_attr(row[field.index])
            setattr(object, field.attribute, value)
            if field.key_field==1:
                if len(self.key_list)==1:
                    object.key = value
                else:
                    object.key = trim(object.key + ' ' + str(value))
        object.in_database = 1
        object.changed = 0

class DataManager(DataTable):
    """
    This class provides high level access to a database table.

    It loads and saves data from the table into an object or a DataSet, which is
    a dictionary of objects. You can request a single object (row), or you can
    specify a set of criteria, which are then translated into a WHERE clause.
    """

    def __init__(self, table_name, field_dictionary):
        DataTable.__init__(self, table_name, field_dictionary)
        
        # FIXME: Look at these when saving!
        self.in_database = 0
        self.changed     = 0
        self.table       = DataTable(table_name, field_dictionary)

    def get_by_id(self, id):
        data_field = self.table.id_field()
        sql = self.table.select + ' WHERE ' + data_field.field_name + '=' + data_field.attr_to_field(id)
        cursor = db.select(sql)
        row = cursor.fetchone()
        if row==None: return
        return self.row_to_object(row)

    def get_by_keys(self, filters):
        wheres = []
        for filter in filters:
            field_name, operator, value = filter
            data_field = self.table.fields[field_name]
            wheres.append(field_name + operator + data_field.attr_to_field(value))
        where = ' WHERE ' + string.join(wheres, ' AND ')
        return self.get_sql(self.table.select + where)

    def get_all(self):
        return self.get_sql(self.table.select)
        
    def get_sql(self, sql):
        set = DataSet(self.dms)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            object = self.row_to_object(row)
            set[object.key] = object
        return set

    def new(self):
        object = self.object_class(self.dms)
        return object

    def row_to_object(self, row):
        object = self.new()
        self.table.load_row(object, row)
        return object

    def save(self, object):
        if object.changed==0:
            print 'Object has not changed.'
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
        db.runsql(sql)
        object.in_database = 1
        object.changed = 0

    def delete(self, object):
        if object.in_database==0:
            return
        wheres = []
        for key in self.table.key_list:
            data_field = self.table.fields[key]
            value = data_field.attr_to_field(getattr(object, data_field.attribute))
            wheres.append(data_field.field_name + '=' + value)
        where = ' WHERE ' + string.join(wheres, ' AND ')
        sql = 'DELETE FROM %s %s' % (self.table.name, where)
        db.runsql(sql)

    def delete_by_keys(self, filters):
        set = self.get_by_keys(filters)
        for key in set.keys():
            object = set[key]
            self.delete(object)
    
    def clear(self, set):
        for key in set.keys():
            self.delete(set[key])

class DataSet(LampadasCollection):

    def __init__(self, dms):
        super(DataSet, self).__init__()
        self.dms = dms

    def average(self, attribute):
        """Returns the average of the requested attribute."""

        if self.count()==0:
            return 0
            
        total = 0
        for key in self.keys():
            object = self[key]
            value = getattr(object, attribute)
            total = total + value
        return total / self.count()

    def max(self, attribute):
        """
        Returns the maximum value of the requested attribute.
        
        This method only supports numeric attributes.
        Returns 0 if there are no objects in the set.
        """

        maximum = 0
        for key in self.keys():
            object = self[key]
            value = getattr(object, attribute)
            maximum = max(maximum, value)
        return maximum

    def min(self, attribute):
        """
        Returns the maximum value of the requested attribute.
        
        This method only supports numeric attributes.
        Returns 0 if there are no objects in the set.
        """

        minimum = 0
        for key in self.keys():
            object = self[key]
            value = getattr(object, attribute)
            minimum = min(minimum, value)
        return minimum
