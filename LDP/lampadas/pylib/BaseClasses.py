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
        self.map         = {}

        self.indexfields   = self.parse_fieldmap(indexfields)
        self.fields        = self.parse_fieldmap(fields)
        self.i18nfields    = self.parse_fieldmap(i18nfields)
        self.allfields     = self.indexfields + self.fields
        self.alli18nfields = self.indexfields + self.i18nfields
        
        self.filters = []

    def parse_fieldmap(self, map):
        if type(map)==types.StringType:
            self.map[map] = map
            return [map]
        elif type(map)==types.DictType:
            for key in map.keys():
                if map[key]:
                    self.map[key] = map[key]
                else:
                    self.map[key] = key
            return map.keys()
        elif type(map)==types.ListType:
            fields = []
            for field in map:
                fields2 = self.parse_fieldmap(field)
                fields += fields2
            return fields

    def load(self):
        LampadasCollection.__init__(self)
        self.load_table()
        if len(self.i18nfields) > 0:
            self.i18ntable = self.table + '_i18n'
            self.load_i18n_table()

    def load_table(self):
        self.select = 'SELECT ' + string.join(self.allfields, ', ') + ' FROM ' + self.table
        cursor = db.select(self.select)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            object = self.object(self)
            object.load_row(row)

            # Build an identifier.
            # If there are multiple key fields, build a string representation instead.
            if len(self.indexfields)==1:
                identifier = convert_field(row[0])
            else:
                identifier = ''
                for field in self.indexfields:
                    value = getattr(object, self.map[field])
                    identifier = identifier + str(value) + ' '
                identifier = trim(identifier)
            object.identifier = identifier
            self[identifier] = object

    def load_i18n_table(self):
        for key in self.keys():
            object = self[key]
            for field in self.i18nfields:
                setattr(object, self.map[field], LampadasCollection())
        sql = 'SELECT ' + string.join(self.indexfields, ', ') + ', lang, ' + string.join(self.i18nfields, ', ') + ' FROM ' + self.i18ntable + ' ORDER BY ' + string.join(self.indexfields, ', ')
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            identifier = convert_field(row[0])
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
                where = ' AND '
            where = where + field + '='
            value = getattr(self, self.parent.map[field])
            type_name = str(type(value))
            if type_name=="<type 'string'>": where += wsq(value)
            elif type_name=="<type 'int'>": where += str(value)
            else: print 'Unrecognized type: ' + type_name
            
        return where

    def load(self):
        # Build an identifier.
        # If there are multiple key fields, build a string representation instead.
        if len(self.parent.indexfields)==1:
            attribute = self.parent.map[self.parent.indexfields[0]]
            identifier = getattr(self, attribute)
        else:
            identifier = ''
            for field in self.parent.indexfields:
                value = getattr(self, self.parentmap[field])
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
            alias = self.parent.map[field]
            value = convert_field(row[i])
            setattr(self, alias, value)
            i += 1

    def load_i18n_row(self, row):
        lang = row[1]
        i = 2
        for field in self.parent.i18nfields:
            value = convert_field(row[i])
            alias = self.parent.map[field]
            coll = getattr(self, alias)
            coll[lang] = value
            setattr(self, field, coll)
            i += 1


class Filter:

    def __init__(self, attribute, operator, value):
        self.attribute = attribute
        self.operator  = operator
        self.value     = value

