#!/usr/bin/python
# 
# This file is part of the Lampadas Documentation System.
# 
# Copyright (c) 2000, 2001, 2002 David Merrill <david@lupercalia.net>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 
"""
These base classes are subclassed by other Lampadas objects,
but are never instantiated directly.
"""

from Globals import *
from Database import db
from Log import log
import string
import copy
import types
import sys
import md5

# TODO: Write testing routines that go through trying to write random data
# into the database while executing random deletes, etc.

class LampadasCollection:
    """
    Base class for Lampadas dictionaries or collection objects.

    Classes based on this one become pseudo-dictionaries, providing
    iteration and similar methods. This is done by providing a wrapper to
    the built-in dictionary type. In Python 2.2, dictionaries will be
    subclassable, so this can be rewritten to take advantage of that.
    """

    def __init__(self):
        self.data = {}

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        try:
            item = self.data[key]
        except KeyError:
            item = None
        return item

    def __setitem__(self, key, item):
        self.data[key] = item

    def __delitem__(self, key):
        del self.data[key]

    def keys(self, attribute=''):
        if attribute=='':
            return self.data.keys()
        keys = []
        for key in self.data.keys():
            object = self[key]
            value = getattr(object, attribute)
            if value not in keys:
                keys.append(value)
        return keys

    def has_key(self, key, attribute=''):
        if attribute=='':
            return self.data.has_key(key)
        for seek_key in self.keys():
            object = self[seek_key]
            value = getattr(object, attribute)
            if value==key:
                return 1
        return 0
    
    def items(self):
        return self.data.items()

    def count(self):
        return len(self.data)

    def sort_by(self, attribute):
        temp, result = [], []
        for key, item in self.items():
            value = getattr(item, attribute)
            temp.append((value, key))
        temp.sort()
        for v,k in temp :
            result.append(k)
        return result

    def sort_by_desc(self, attribute):
        temp, result = [], []
        for key, item in self.items():
            value = getattr(item, attribute)
            temp.append((value, key))

        # Must sort before calling reverse()!
        temp.sort()
        temp.reverse()
        for v,k in temp :
            result.append(k)
        return result

    def sort_by_lang(self, attribute, lang):
        for key in self.keys():
            item = self.data[key]
            value = getattr(item, attribute)
            langvalue = value[lang]
            item.sort_order = langvalue
        return self.sort_by('sort_order')

class DataFields(LampadasCollection):
    
    def primary_keys(self):
        keys = []
        for key in self.sort_by('field_name'):
            data_field = self[key]
            if data_field.primary==1:
                keys.append(key)
        return keys

    def nonprimary_keys(self):
        keys = []
        for key in self.sort_by('field_name'):
            data_field = self[key]
            if data_field.primary==0:
                keys.append(key)
        return keys

    def find_attribute(self, attribute):
        for key in self.keys():
            if self[key].attribute==attribute:
                return self[key]

class DataField:

    def __init__(self, field_name='', data_type='', attribute='', primary=0, nullable=1):
        self.field_name = field_name
        self.data_type  = data_type
        self.attribute  = attribute
        self.primary    = primary
        self.nullable   = nullable
        if self.attribute=='':
            self.attribute = self.field_name
   
    def default(self):
        if self.data_type in ('string', ''):      return ''
        elif self.data_type in ('sequence', 'int', 'float'):  return 0
        elif self.data_type=='time':              return ''
        elif self.data_type=='date':              return ''
        elif self.data_type=='bool':              return 0
        elif self.data_type=='created':           return now_string()
        elif self.data_type=='updated':           return None
        elif self.data_type=='creator':           return None
        elif self.data_type=='updater':           return None
        else:
            print 'Unrecognized type: ' + self.data_type
            sys.exit(1)
        
    def field_to_attr(self, value):
        if self.data_type in ('string', ''):      return trim(value)
        elif self.data_type in ('sequence', 'int', 'float'):  return safeint(value)
        elif self.data_type=='time':              return time2str(value)
        elif self.data_type=='date':              return date2str(value)
        elif self.data_type=='bool':              return tf2bool(value)
        elif self.data_type=='created':           return time2str(value)
        elif self.data_type=='updated':           return time2str(value)
        elif self.data_type=='creator':           return trim(value)
        elif self.data_type=='updater':           return trim(value)
        else:
            print 'Unrecognized type: ' + self.data_type
            sys.exit(1)

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
        else:
            print 'ERROR: Unrecognized data type definition, see DataObject.attr_to_field()'
            print 'Table= ' + self.parent.table
            print 'Data= ' + str(key)
            print 'Data Type (INVALID): ' + str(data_type)
            sys.exit(1)

class DataCollection(LampadasCollection):

    def __init__(self, parent_collection, object, table, indexfields, fields, i18nfields, cache_size=-1):
        """
        cache_size determines how many items are held in the collection cache.
        0 means no caching at all; -1 means cache everything.
        """
         
        LampadasCollection.__init__(self)
        self.parent_collection = parent_collection
        self.child_collections = []
        self.object      = object
        self.table       = table
        self.filters     = []
        self.indexfields = []
        self.fields      = []
        self.i18nfields  = []
        self.cache_size  = cache_size

        # All index files are *automatically* set to be primary
        self.map         = DataFields()
        self.indexfields   = self.parse_fieldmap(indexfields)
        for key in self.map.keys():
            self.map[key].primary = 1
        self.fields        = self.parse_fieldmap(fields)
        self.i18nfields    = self.parse_fieldmap(i18nfields)
        self.allfields     = self.indexfields + self.fields
        self.alli18nfields = self.indexfields + self.i18nfields
        self.idfields      = self.indexfields[:]

        self.select = 'SELECT ' + string.join(self.allfields, ', ') + ' FROM ' + self.table
        self.updated = None

    def __getitem__(self, key):
        """If the collection has never been loaded, we load each object on demand. """
        object = LampadasCollection.__getitem__(self, key)
        if object==None:
            object = self.object(self)
            values = string.split(str(key), ' ')
            i = 0
            for field in self.indexfields:
                data_field = self.map[field]
                value = data_field.field_to_attr(values[i])
                i += 1
                setattr(object, data_field.attribute, value)
            if object.load()==0:
                return None
            self[object.id] = object
        object.cache_requested = now_string()
        return object

    def __setitem__(self, key, item):
        if self.can_cache()==0:
            return
        elif self.cache_full()==1:
            removed_count = 0
            for key in self.sort_by('cache_requested'):
                del self[key]
                removed_count += 1
                if removed_count==CACHE_REMOVAL_DELTA:
                    break
        item.cache_created = now_string()
        self.data[key] = item

    def keys(self, attribute=''):
        if self.cache_unlimited()==1:
            if not self.parent_collection==None:
                self.refresh_filters()
            return LampadasCollection.keys(self, attribute)

        # If we're not searching for an attribute, do a quick scan of
        # only the id fields. Let the db do DISTINCT.
        keys = []
        if attribute=='':
            fields = []
            for field in self.idfields:
                data_field = self.map[field]
                fields.append(data_field.field_name)
            sql = 'SELECT DISTINCT ' + string.join(fields, ', ') + ' FROM ' + self.table + ' ' + self.where()
            cursor = db.select(sql)
            while (1):
                row = cursor.fetchone()
                if row==None: break
                if len(self.idfields)==1:
                    key = self.map[string.join(self.idfields)].field_to_attr(row[0])
                else:
                    key = ''
                    i = 0
                    for field in self.idfields:
                        value = self.map[field].field_to_attr(row[i])
                        key = key + ' ' + str(value)
                        i += 1
                    key = trim(key)
                keys.append(key)
        else:
            for field in self.fields:
                data_field = self.map[field]
                if data_field.attribute==attribute:
                    field_name = data_field.field_name
            data_field = self.map[field_name]
            sql = 'SELECT DISTINCT ' + field_name + ' FROM ' + self.table + ' ' + self.where()
            cursor = db.select(sql)
            while (1):
                row = cursor.fetchone()
                if row==None: break
                key = data_field.field_to_attr(row[0])
                keys.append(key)
        return keys
    
    def count(self):
        """Read from the database, because we might not have all data loaded."""

        # db.count()'s where clause does not expect the word WHERE, so remove it first.
        where_clause = self.where()
        where_clause = where_clause.replace(' WHERE ', '')
        return int(db.count(self.table, where_clause))

    def can_cache(self):
        return self.cache_size <> 0

    def cache_full(self):
        return self.cache_size==len(self.data)

    def cache_unlimited(self):
        return self.cache_size==-1
        
    def where(self):
        """Examine the filters we have on us, and build an equivalent WHERE clause."""
        where_string = ''
        if self.parent_collection==None:
            return ''

        for filter in self.filters:
            filter.refresh_value()
            child_attr = filter.child_attr
            value = filter.value
            data_field = self.map.find_attribute(child_attr)
            assert not data_field==None
            value = data_field.attr_to_field(filter.value)
            if where_string=='':
                where_string = ' WHERE '
            else:
                where_string += ' AND '
            where_string = where_string + data_field.field_name + filter.operator
            where_string += value
        return where_string

    def parse_fieldmap(self, map):

        # Just a field name
        # A complete dictionary of field properties
        if type(map)==types.DictType:
            if len(map.keys()) > 1:
                print 'ERROR: There should only be a single key here.'
                print 'This is probably an error in a data structure definition.'
                print
                print 'table: ' + self.table
                print 'map keys: ' + str(map.keys())
            key = string.join(map.keys())
            if self.map.has_key(key)==0:
                self.map[key] = DataField(field_name=key)
            oldmap = map[key]
            newmap = self.map[key]
            if type(oldmap)==types.DictType:
                for key in oldmap.keys():
                    value = oldmap[key]
                    if key=='data_type':   newmap.data_type = value
                    elif key=='attribute': newmap.attribute = value
                    elif key=='primary':   newmap.primary   = value
                    elif key=='nullable':  newmap.nullable  = value
                    else:
                        print 'ERROR: Unrecognized DataField key: ' + key
                        sys.exit(1)
            else:
                newmap.field_name = oldmap
            return map.keys()

        # A list of field names.
        elif type(map)==types.ListType:
            fields = []
            for field in map:
                fields2 = self.parse_fieldmap(field)
                fields += fields2
            return fields
        else:
            print 'ERROR: Unrecognized data definition type, ' + str(type(map))
            print 'Table= ' + self.table
            print 'Data= ' + str(map)
            sys.exit(1)

    def reload(self):
        self.load(self.updated)

    def load(self, updated=''):
        if self.parent_collection==None:
            # Do not load collection if current size has reached cache_size
            if self.can_cache()==0 or self.cache_full()==1:
                return
            self.updated = now_string()
            #print self.count()
            #print 'Loading ' + self.table + ' since ' + updated + '...'
            if updated > '':
                sql = 'SELECT identifier FROM deleted WHERE table_name=' + wsq(self.table) + ' AND deleted >= ' + wsq(updated)
                #print sql
                cursor = db.select(sql)
                while (1):
                    row = cursor.fetchone()
                    if row==None: break
                    identifier = row[0]
                    id_type = 'int'
                    for field in self.indexfields:
                        if self.map[field].data_type in ('string',):
                            id_type = 'string'
                    if id_type=='int':
                        identifier = int(identifier)
                    else:
                        identifier = trim(identifier)
                    #print 'Object identifier: ' + str(identifier) + ' has been deleted.'
                    object = self[identifier]
                    id = object.build_id(self.idfields)
                    self.delete(id)
                #print 'Done handling deletions, count: ' + trim(self.count())
                where_clause = ' WHERE updated >= ' + wsq(updated)
            else:
                where_clause = ''
            self.load_table(where_clause)
            if len(self.i18nfields) > 0:
                self.i18ntable = self.table + '_i18n'
                self.load_i18n_table()
            #print 'Done loading ' + self.table + ', count: ' + trim(self.count()) + ', len(self.data): ' + str(len(self.data))
        else:
            self.parent_collection.load(updated)
            self.refresh_filters()

    def load_table(self, where_clause=''):
        sql = self.select + where_clause
        #print sql
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            object = self.object(self)
            object.load_row(row)
            self[object.id] = object
            #print self.table + ', ' + str(object.id)

    def load_i18n_table(self, where_clause=''):
        for key in self.keys():
            object = self[key]
            for field in self.i18nfields:
                setattr(object, self.map[field].attribute, LampadasCollection())
        sql = 'SELECT ' + string.join(self.indexfields, ', ') + ', lang, ' + string.join(self.i18nfields, ', ') + ' FROM ' + self.i18ntable + where_clause + ' ORDER BY ' + string.join(self.indexfields, ', ')
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            data_field = self.map[string.join(self.map.primary_keys())]
            id = data_field.field_to_attr(row[0])
            object = self[id]
            object.load_i18n_row(row)

    def add(self, object):
        if self.parent_collection==None:
            object.parent = self
            for field in self.indexfields:
                data_field = self.map[field]
                if data_field.data_type=='sequence':
                    new_id = db.next_id(self.table, data_field.field_name)
                    setattr(object, data_field.attribute, new_id)
            sql = 'INSERT INTO %s (%s) VALUES (%s)' % (self.table, object.fields(), object.values())
            db.runsql(sql)
            db.commit()
            object.id = object.build_id(self.idfields)
            self[object.id] = object
            #self.refresh_children()
        else:
            self.parent_collection.add(object)
            self.refresh_filters()
        return object

    def clear(self):
        item_count = self.count()
        for key in self.keys():
            self.delete(key)
            item_count = item_count - 1
            assert item_count==self.count(), 'Just deleted an item, should have ' + str(item_count) + ' items, but have ' + str(self.count())
        self.refresh_filters()

    def delete(self, key):
        object = self[key]
        if self.parent_collection==None:
            for child_key in object.child_collections.keys():
                child_collection = object.child_collections[child_key]
                child_collection.clear()
            object.delete()
            del self[key]
            #self.refresh_children()
        else:
            id = object.build_id(self.parent_collection.idfields)
            self.parent_collection.delete(id)
            self.refresh_filters()
        
    def save(self):
        for key in self.keys():
            object = self[key]
            object.save()
            
    def refresh_keys(self):
        for key in self.keys():
            object = self[key]
            object.id = object.build_id(self.idfields)
            if object.id <> key:
                del self[key]
                self[object.id] = object

    def apply_filter(self, superclass, filter):
        """
        Filter the collection for the requested pattern.

        This routine supports up to two key fields. Whichever field was not
        requested in the filter is returned as the key field in the resultset.
        """

        # TODO: Generate the search form using the filter information,
        # so the filter can easily be displayed and refined.
        
        # TODO: Write subclasses to generate search forms,
        # list forms (including the DocTable), edit forms
        # and add forms. Subclass Table as well, and add to
        # the tables collection.

        # TODO: Add ability to add, edit and delete any of the filters.

        # TODO: Add the ability to name and save a set of filters.

        filter_results = superclass()
        filter_results.parent_collection = self
        self.child_collections.append(filter_results)
        filter_results.filters.append(filter)
        # If the requested filter field is also an id field,
        # assume it is no longer desired as an id field --
        if filter.child_attr in filter_results.idfields:
            filter_results.idfields.remove(filter.child_attr)
            assert len(filter_results.idfields)==1
        return filter_results

    def refresh_filters(self):
        # FIXME: Replace with the filter() function, which is much faster.

        values = []
        for filter in self.filters:
            filter.refresh_value()
            values.append(str(filter.value))
            
        #print self.table + '.refresh_filters(), ' + string.join(values, ' ')
        # Start with all of our parent's objects
        self.updated = self.parent_collection.updated
        self.data = {}
        for key in self.parent_collection.keys():
            object = self.parent_collection[key]

            all_match = 1
            for filter in self.filters:
                filter.refresh_value()
                value = getattr(object, filter.child_attr)
                if filter.operator=='=':    match = (value == filter.value)
                elif filter.operator=='<>': match = (value <> filter.value)
                elif filter.operator=='>':  match = (value >  filter.value)
                elif filter.operator=='<':  match = (value <  filter.value)
                else:
                    log(1, 'Unrecognized filter operator')
                    print 'ERROR: Unrecognized filter in refresh_filters()'
                    sys.exit(1)
                if match==0:
                    all_match = 0
                    break
            if all_match==1:
                object.id = object.build_id(self.idfields)
                self[object.id] = object

    def refresh_children(self):
        for child in self.child_collections:
            child.refresh_filters()

class DataObject:

    def __init__(self, parent):
        self.parent = parent
        self.md5 = ''
        self.cache_created = ''
        self.cache_requested = ''
        for field in self.parent.allfields:
            data_field = self.parent.map[field]
            setattr(self, data_field.attribute, data_field.default())
        self.child_collections = LampadasCollection()

    def calculate_md5(self):
        m = md5.new()
        for field in self.parent.allfields:
            data_field = self.parent.map[field]
            value = str(getattr(self, data_field.attribute))
            m.update(value)
        return m.hexdigest()

    def add_child(self, child_name, child_collection):
        setattr(self, child_name, child_collection)
        self.child_collections[child_name] = child_collection
    
    def refresh_children(self):
        for child in self.child_collections:
            child.refresh_filters()
            
    def where(self):
        where_string = ''
        for field in self.parent.indexfields:
            if where_string=='':
                where_string = ' WHERE '
            else:
                where_string += ' AND '
            where_string = where_string + field + '='
            map = self.parent.map[field]
            value = getattr(self, map.attribute)
            where_string += map.attr_to_field(value)
        return where_string

    def fields(self):
        field_list = []
        for field in self.parent.allfields:
            map = self.parent.map[field]
            if map.data_type not in ('created', 'updated'):
                field_list.append(field)
        return string.join(field_list, ', ')

    def values(self):
        value_list = []
        for field in self.parent.allfields:
            map = self.parent.map[field]
            if map.data_type not in ('created', 'updated'):
                value_list.append(map.attr_to_field(getattr(self, map.attribute)))
        return string.join(value_list, ', ')
    
    def build_id(self, build_idfields=None):
        # Build an identifier.
        # If there are multiple id fields, build a string representation instead.

        # FIXME: Subtle problem, an object can have more than one id if it belongs
        # to more than one collection with different keys! Not a propblem as long
        # as users of the value always get it recalculated before using it.

        if build_idfields==None:
            idfields = self.parent.idfields
        else:
            idfields = build_idfields
        if len(idfields)==1:
            map = self.parent.map[idfields[0]]
            id = getattr(self, map.attribute)
        else:
            id = ''
            for idfield in idfields:
                value = getattr(self, self.parent.map[idfield].attribute)
                id = id + str(value) + ' '
            id = trim(id)
        return id
            
    def load(self):
        self.select = self.parent.select + self.where()
        cursor = db.select(self.select)
        row = cursor.fetchone()
        if row==None: return 0
        self.load_row(row)
        return 1

    def load_row(self, row):
        i = 0
        for field in self.parent.allfields:
            data_field = self.parent.map[field]
            attribute = data_field.attribute
            value = data_field.field_to_attr(row[i])
            setattr(self, attribute, value)
            i += 1
        self.id = self.build_id(self.parent.idfields)
        self.md5 = self.calculate_md5()

    def load_i18n_row(self, row):
        lang = row[1]
        i = 2
        for field in self.parent.i18nfields:
            value = self.parent.map[field].field_to_attr(row[i])
            attribute = self.parent.map[field].attribute
            coll = getattr(self, attribute)
            coll[lang] = value
            setattr(self, field, coll)
            i += 1
        self.md5 = self.calculate_md5()

    def save(self):
        new_md5 = self.calculate_md5()
        if new_md5 <> self.md5:
            field_list = []
            sql = WOStringIO('UPDATE %s SET ' % self.parent.table)
            for key in self.parent.map.keys():
                data_field = self.parent.map[key]
                value = getattr(self, data_field.attribute)
                value = data_field.attr_to_field(value)
                field_list.append('%s=%s' % (key, value))
            sql.write(string.join(field_list, ', '))
            sql.write(self.where())
            db.runsql(sql.get_value())
            db.commit()
            self.md5 = self.calculate_md5()
        
    def delete(self):
        sql = 'DELETE FROM ' + self.parent.table + self.where()
        #print sql
        db.runsql(sql)
        db.commit()
        sql = 'INSERT INTO deleted(table_name, identifier) VALUES (%s, %s)' % (wsq(self.parent.table), wsq(str(self.build_id())))
        db.runsql(sql)
        db.commit()

class Filter:

    def __init__(self, parent, parent_attr, operator, child_attr):
        self.parent      = parent
        self.parent_attr = parent_attr
        self.operator    = operator
        self.child_attr  = child_attr
        self.refresh_value()

    def refresh_value(self):
        self.value = getattr(self.parent, self.parent_attr)
