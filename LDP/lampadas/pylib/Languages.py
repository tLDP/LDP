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

from Globals import *
from BaseClasses import *
from Database import db

class Languages(LampadasCollection):
    """
    A collection object of all languages supported by the ISO 639
    standard.
    """

    def __init__(self):
        self.data = {}
        self.supported = []

    def load(self):
        sql = "SELECT lang_code, supported FROM language"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            language = Language()
            language.load_row(row)
            self.data[language.code] = language
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT lang_code, lang, lang_name FROM language_i18n"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            lang_code = trim(row[0])
            lang      = trim(row[1])
            language  = self[lang_code]
            language.name[lang] = trim(row[2])

    def supported_keys(self, lang):
        if len(self.supported)==0:
            self.supported = []
            for key in self.sort_by_lang('name', lang):
                if self[key].supported==1:
                    self.supported = self.supported + [key]
        return self.supported

class Language:
    """
    Defines a language supported by Lampadas. Documents can be translated into,
    and Lampadas can be localized for, any language supported by ISO 639.
    """

    def __init__(self):
        self.name = LampadasCollection()

    def load_row(self, row):
        self.code      = trim(row[0])
        self.supported = tf2bool(row[1])


languages = Languages()
languages.load()
