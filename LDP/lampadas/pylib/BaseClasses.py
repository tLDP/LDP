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
        result = []
        for key, item in self.items():
            value = getattr(item, attribute)
            result.append((value, key))
        result.sort()
        for i in xrange(len(result)):
            result[i] = result[i][1]
        return result

    def sort_by_desc(self, attribute):
        result = []
        for key, item in self.items():
            value = getattr(item, attribute)
            result.append((value, key))
        result.reverse()
        for i in xrange(len(result)):
            result[i] = result[i][1]
        return result

    def sort_by_lang(self, attribute, lang):
        keys = self.keys()
        for key in keys:
            item = self.data[key]
            value = getattr(item, attribute)
            langvalue = value[lang]
            item.sort_order = langvalue
        return self.sort_by('sort_order')

