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

# ErrorTypes

class ErrorTypes(LampadasCollection):
    """A collection of error types."""

    def __init__(self):
        self.data = {}
    
    def load(self):
        sql = 'SELECT err_type_code FROM error_type'
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            errtype = ErrorType()
            errtype.load_row(row)
            self[errtype.code] = errtype
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT err_type_code, lang, err_type_name, err_type_desc FROM error_type_i18n"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            err_type_code              = trim(row[0])
            errtype = self[err_type_code]
            lang                       = trim(row[1])
            errtype.name[lang]         = trim(row[2])
            errtype.description[lang]  = trim(row[3])

class ErrorType:

    def __init__(self, code=''):
        self.code        = ''
        self.name        = LampadasCollection()
        self.description = LampadasCollection()
       
    def load_row(self, row):
        self.code = trim(row[0])

errortypes      = ErrorTypes()
errortypes.load()
