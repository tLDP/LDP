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

    def convert_field(self, value):
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

# TODO: Write add(), delete() and update() methods.

# TODO: Use a database table to log changed objects, and have DataCollection
# objects poll for updates during page loads. To fix broken caching.

class DataCollection(LampadasCollection):

    def __init__(self, object=None, table='', indexfields=[], fields=[], i18nfields=[], filter=None):
        LampadasCollection.__init__(self)
        self.object      = object
        self.table       = table
        self.origindex   = indexfields
        self.origfields  = fields
        self.origi18n    = i18nfields
        self.filter      = filter
        
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

        self.select = 'SELECT ' + string.join(self.allfields, ', ') + ' FROM ' + self.table
        self.filters = []

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

    def load(self):
        LampadasCollection.__init__(self)
        self.load_table()
        if len(self.i18nfields) > 0:
            self.i18ntable = self.table + '_i18n'
            self.load_i18n_table()

    def load_table(self):
        cursor = db.select(self.select)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            object = self.object(self)
            object.load_row(row)

            # Build an identifier.
            # If there are multiple key fields, build a string representation instead.
            if len(self.indexfields)==1:
                identifier = self.map[self.indexfields[0]].convert_field(row[0])
            else:
                identifier = ''
                for field in self.indexfields:
                    value = getattr(object, self.map[field].attribute)
                    identifier = identifier + str(value) + ' '
                identifier = trim(identifier)
            object.identifier = identifier
            self[identifier] = object

    def load_i18n_table(self):
        for key in self.keys():
            object = self[key]
            for field in self.i18nfields:
                setattr(object, self.map[field].attribute, LampadasCollection())
        sql = 'SELECT ' + string.join(self.indexfields, ', ') + ', lang, ' + string.join(self.i18nfields, ', ') + ' FROM ' + self.i18ntable + ' ORDER BY ' + string.join(self.indexfields, ', ')
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            data_field = self.map[string.join(self.map.primary_keys())]
            identifier = data_field.convert_field(row[0])
            object = self[identifier]
            object.load_i18n_row(row)

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
        filter_results.filters.append(filter)
        for key in self.keys():
            object = self[key]
            value = getattr(object, filter.attribute)
            match = 0
            if filter.operator=='=':    match = (value == filter.value)
            elif filter.operator=='<>': match = (value <> filter.value)
            elif filter.operator=='>':  match = (value >  filter.value)
            elif filter.operator=='<':  match = (value <  filter.value)
            else: log(1, 'Unrecognized filter operator')
            if match==1:
                identifier = object.identifier
                filter_results[identifier] = object
        return filter_results


class DataObject:

    def __init__(self, parent):
        self.parent = parent

    def where(self):
        where = ''
        for field in self.parent.indexfields:
            if where=='':
                where = ' WHERE '
            else:
                where += ' AND '
            where = where + field + '='
            value = getattr(self, self.parent.map[field].attribute)
            type_name = str(type(value))
            if type_name=="<type 'string'>": where += wsq(value)
            elif type_name=="<type 'int'>": where += str(value)
            else:
                print 'Unrecognized type: ' + type_name
                sys.exit(1)
            
        return where

    def load(self):
        # Build an identifier.
        # If there are multiple key fields, build a string representation instead.
        if len(self.parent.indexfields)==1:
            map = self.parent.map[self.parent.indexfields[0]]
            identifier = getattr(self, map.attribute)
        else:
            identifier = ''
            for field in self.parent.indexfields:
                value = getattr(self, self.parent.map[field])
                identifier = identifier + str(value) + ' '
            identifier = trim(identifier)
        self.identifier = identifier
        self.select = self.parent.select + self.where()
        cursor = db.select(self.select)
        row = cursor.fetchone()
        if row==None:
            # FIXME: We have to delete ourselves
            del self.parent[self.identifier]
        else:
            self.load_row(row)

    def load_row(self, row):
        i = 0
        for field in self.parent.allfields:
            attribute = self.parent.map[field].attribute
            value = self.parent.map[field].convert_field(row[i])
            setattr(self, attribute, value)
            i += 1

    def load_i18n_row(self, row):
        lang = row[1]
        i = 2
        for field in self.parent.i18nfields:
            value = self.parent.map[field].convert_field(row[i])
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
            data_type = data_field.data_type
            if data_type in ('int', 'float'):
                if data_field.nullable==1 and value==0:
                    replacement = 'NULL'
                else:
                    replacement = str(value)
            elif data_type=='bool':
                replacement = wsq(bool2tf(value))
            elif data_type=='string':
                replacement = wsq(str(value))
            elif data_type=='date':
                replacement = wsq(str(value))
            elif data_type=='time':
                replacement = wsq(str(value))
            elif data_type=='created':
                replacement = wsq(str(value))
            elif data_type=='updated':
                replacement = wsq(now_string())
            else:
                print 'ERROR: Unrecognized data type definition, see DataObject.save()'
                print 'Table= ' + self.parent.table
                print 'Data= ' + str(key)
                print 'Data Type (INVALID): ' + str(data_type)
                sys.exit(1)
            field_list.append('%s=%s' % (key, replacement))
        sql.write(string.join(field_list, ', '))
        sql.write(self.where())
        #print sql.get_value()
        db.runsql(sql.get_value())
                
            

class Filter:

    def __init__(self, attribute, operator, value):
        self.attribute = attribute
        self.operator  = operator
        self.value     = value

