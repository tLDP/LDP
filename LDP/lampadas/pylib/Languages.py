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
Holds a collection of ISO languages.
"""

from BaseClasses import *

class Languages(DataCollection):
    """
    A collection object of all languages supported by the ISO 639
    standard.
    """

    def __init__(self):
        DataCollection.__init__(self, None, Language,
                                'language',
                                {'lang_code':  {'data_type': 'string', 'attribute': 'code'}},
                                [{'encoding':  {'data_type': 'string'}},
                                 {'supported': {'data_type': 'bool'}},
                                 {'created':   {'data_type': 'created'}},
                                 {'updated':   {'data_type': 'updated'}}],
                                {'lang_name':  {'data_type': 'string', 'attribute': 'name'}})

    # TODO: Replace with a reusable filtering system in DataCollection
    def supported_keys(self, lang=''):
        supported = LampadasCollection()
        for key in self.keys():
            language = self[key]
            if language.supported==1:
                language.own_name = language.name[language.code]
                supported[language.code] = language

        if lang > '':
            keys = supported.sort_by_lang('name', lang)
        else:
            keys = supported.sort_by('own_name')
        
        return keys
    

class Language(DataObject):
    """
    Defines a language supported by Lampadas. Documents can be translated into,
    and Lampadas can be localized for, any language supported by ISO 639.
    """
    pass

languages = Languages()
languages.load()

#for key in languages.keys():
#    language = languages[key]
#    print 'Language: ' + language.code + ', name: ' + language.name['EN']
