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

from Globals import *
from BaseClasses import *
from Database import db

# Errors

class Errors(TableCollection):
    """
    A collection object of all errors that can be filed against a document.
    """
    
    def __init__(self):
        TableCollection.__init__(self, Error,
                                 'error',
                                 {'err_id': 'id'},
                                 ['err_type_code', 'created', 'updated'],
                                 {'err_name': 'name', 'err_desc': 'description'})
        
class Error:
    """
    An error that can be filed against a document.
    """
    pass
    
errors = Errors()
errors.load()
