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

class LampadasCollection(dict):
    """
    Base class for Lampadas dictionaries or collection objects.

    Classes based on this one become pseudo-dictionaries, providing
    iteration and similar methods. This is done by providing a wrapper to
    the built-in dictionary type. In Python 2.2, dictionaries will be
    subclassable, so this can be rewritten to take advantage of that.
    """

    def keys(self, attribute=''):
        if attribute=='':
            return super(LampadasCollection, self).keys()
        keys = []
        for key in super(LampadasCollection, self).keys():
            object = self[key]
            value = getattr(object, attribute)
            if value not in keys:
                keys.append(value)
        return keys

    def has_key(self, key, attribute=''):
        if attribute=='':
            return super(LampadasCollection, self).has_key(key)
        for seek_key in self.keys():
            object = self[seek_key]
            value = getattr(object, attribute)
            if value==key:
                return 1
        return 0

    def count(self):
        return len(self)

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
            item = self[key]
            value = getattr(item, attribute)
            langvalue = value[lang]
            item.sort_order = langvalue
        return self.sort_by('sort_order')
