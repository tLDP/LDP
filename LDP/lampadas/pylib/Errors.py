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

from Globals import *
from BaseClasses import *
from Database import db

# Errors

class Errors(LampadasCollection):
    """
    A collection object of all errors that can be filed against a document.
    """
    
    def __init__(self):
        self.data = {}
        
    def load(self):
        self.data = {}
        sql = "SELECT err_id, err_type_code FROM error"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            err = Error()
            err.load_row(row)
            self.data[err.id] = err
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT err_id, lang, err_name, err_desc FROM error_i18n"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            err_id                 = row[0]
            err = self[err_id]
            lang                   = row[1]
            err.name[lang]         = trim(row[2])
            err.description[lang]  = trim(row[3])

class Error:
    """
    An error that can be filed against a document.
    """
    
    def __init__(self, id=0, err_type_code=''):
        self.id            = id
        self.err_type_code = err_type_code
        self.name          = LampadasCollection()
        self.description   = LampadasCollection()

    def load_row(self, row):
        self.id            = row[0]
        self.err_type_code = trim(row[1])

errors = Errors()
errors.load()
