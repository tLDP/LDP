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

# TODO: Write testing routines that go through trying to write random data into the database
# whilc executing random deletes, etc.

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

class DataField:

    def __init__(self, field_name='', data_type='', attribute='', primary=0, nullable=1):
        self.field_name = field_name
        self.data_type  = data_type
        self.attribute  = attribute
        self.primary    = primary
        self.nullable   = nullable
        if self.attribute=='':
            self.attribute = self.field_name
   
    def __call__(self):
        return self.attribute

    def field_to_attr(self, value):
        if self.data_type in ('string', ''):      return trim(value)
        elif self.data_type in ('int', 'float'):  return safeint(value)
        elif self.data_type=='time':              return time2str(value)
        elif self.data_type=='date':              return date2str(value)
        elif self.data_type=='bool':              return tf2bool(value)
        elif self.data_type=='created':           return time2str(value)
        elif self.data_type=='updated':           return time2str(value)
        else:
            print 'Unrecognized type: ' + type_name
            sys.exit(1)

    def attr_to_field(self, value):
        if self.data_type in ('int', 'float'):
            if self.nullable==1 and value==0:
                return 'NULL'
            else:
                return str(value)
        elif self.data_type=='bool':    return wsq(bool2tf(value))
        elif self.data_type=='string':  return wsq(str(value))
        elif self.data_type=='date':    return wsq(str(value))
        elif self.data_type=='time':    return wsq(str(value))
        elif self.data_type=='created': return wsq(str(value))
        elif self.data_type=='updated': return wsq(now_string())
        else:
            print 'ERROR: Unrecognized data type definition, see DataObject.attr_to_field()'
            print 'Table= ' + self.parent.table
            print 'Data= ' + str(key)
            print 'Data Type (INVALID): ' + str(data_type)
            sys.exit(1)

class DataCollection(LampadasCollection):

    def __init__(self, parent_collection, object, table, indexfields, fields, i18nfields):
        LampadasCollection.__init__(self)
        self.parent_collection = parent_collection
        self.child_collections = []
        self.object      = object
        self.table       = table
        self.filters     = []
        self.indexfields = []
        self.fields      = []
        self.i18nfields  = []
        self.map         = DataFields()

        # All index files are *automatically* set to be primary
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
            #original_count = self.count()
            self.updated = now_string()
            #print self.count()
            #print 'Loading since ' + updated + '...'
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
            #print 'Done handling updates, count: ' + trim(self.count())
            #if self.count() <> original_count:
                #print 'Counts differ: ' + str(self.count()) + ' from original ' + str(original_count)
                #self.refresh_children()
        else:
            self.parent_collection.load(updated)

    def load_table(self, where_clause=''):
        cursor = db.select(self.select + where_clause)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            object = self.object(self)
            object.load_row(row)
            self[object.id] = object

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
            sql = 'INSERT INTO %s (%s) VALUES (%s)' % (self.table, object.fields(), object.values())
            db.runsql(sql)
            db.commit()
            object.id = object.build_id(self.idfields)
            self[object.id] = object
            #self.refresh_children()
        else:
            self.parent_collection.add(object)
            self.refresh_filters()

    def clear(self):
        for key in self.keys():
            self.delete(key)
        self.refresh_filters()

    def delete(self, key):
        object = self[key]
        if self.parent_collection==None:
            object.delete()
            del self[key]
            #self.refresh_children()
        else:
            id = object.build_id(self.parent_collection.idfields)
            self.parent_collection.delete(id)
            self.refresh_filters()
        
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
        if filter.attribute in filter_results.idfields:
            filter_results.idfields.remove(filter.attribute)
            assert len(filter_results.idfields)==1
            self.refresh_keys()
        filter_results.refresh_filters()
        return filter_results

    def refresh_filters(self):
        # FIXME: Replace with the filter() function, which is much faster.

        # Start with all of our parent's objects
        self.updated = self.parent_collection.updated
        self.data = {}
        for key in self.parent_collection.keys():
            object = self.parent_collection[key]

            all_match = 1
            for filter in self.filters:
                value = getattr(object, filter.attribute)
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

    def __init__(self, parent=None):
        self.parent = parent

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
                value_list.append(map.attr_to_field(getattr(self, field)))
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
        self.load_row(row)

    def load_row(self, row):
        i = 0
        for field in self.parent.allfields:
            attribute = self.parent.map[field].attribute
            value = self.parent.map[field].field_to_attr(row[i])
            setattr(self, attribute, value)
            i += 1
        self.id = self.build_id(self.parent.idfields)

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

    def save(self):
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
        
    def delete(self):
        sql = 'DELETE FROM ' + self.parent.table + self.where()
        db.runsql(sql)
        sql = 'INSERT INTO deleted(table_name, identifier) VALUES (%s, %s)' % (wsq(self.parent.table), wsq(str(self.build_id())))
        db.runsql(sql)

class Filter:

    def __init__(self, attribute, operator, value):
        self.attribute = attribute
        self.operator  = operator
        self.value     = value

