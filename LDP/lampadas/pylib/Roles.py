#/usr/bin/python
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

from BaseClasses import *

# Roles

class Roles(DataCollection):
    """
    A collection object of all roles.
    """
    
    def __init__(self):
        DataCollection.__init__(self, Role,
                                 'role',
                                 {'role_code': 'code'},
                                 [],
                                 {'role_name': 'name', 'role_desc': 'description'})

class Role(DataObject):
    """
    A role is a way of identifying the role a user plays in the production
    of a document.
    """
    pass

roles = Roles()
roles.load()
