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
import string
import types

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

    def keys(self):
        return self.data.keys()

    def has_key(self, key):
        return self.data.has_key(key)
    
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


class TableCollection(LampadasCollection):

    def __init__(self, object=None, table='', indexfields=[], fields=[], i18nfields=[]):
        LampadasCollection.__init__(self)
        self.object      = object
        self.table       = table
        self.indexfields = []
        self.fields      = []
        self.i18nfields  = []
        self.map         = {}

        self.indexfields   = self.parse_fieldmap(indexfields)
        self.fields        = self.parse_fieldmap(fields)
        self.i18nfields    = self.parse_fieldmap(i18nfields)
        self.allfields     = self.indexfields + self.fields
        self.alli18nfields = self.indexfields + self.i18nfields

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
        sql = 'SELECT ' + string.join(self.allfields, ', ') + ' FROM ' + self.table
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            identifier = self.convert_field(row[0])
            object = self.object()
            i = 0
            for field in self.allfields:
                alias = self.map[field]
                value = self.convert_field(row[i])
                setattr(object, alias, value)
                i += 1
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
            identifier = self.convert_field(row[0])
            lang = row[1]
            object = self[identifier]
            i = 2
            for field in self.i18nfields:
                value = self.convert_field(row[i])
                alias = self.map[field]
                coll = getattr(object, alias)
                coll[lang] = value
                setattr(object, field, coll)
                i += 1

    def convert_field(self, value):
        type_name = str(type(value))
        if type_name=="<type 'string'>":
            return trim(value)
        elif type_name=="<type 'int'>":
            return safeint(value)
        elif type_name=="<type 'DateTime'>":
            return time2str(value)
        elif type_name=="<type 'libpq.PgBoolean'>":
            return tf2bool(value)
        else:
            print 'Unrecognized type: ' + type_name

