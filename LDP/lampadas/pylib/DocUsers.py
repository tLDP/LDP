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

from BaseClasses import *

class DocUsers(DataCollection):
    """
    A collection object providing access to all document volunteers.
    """

    def __init__(self):
        DataCollection.__init__(self, None, DocUser,
                                 'document_user',
                                 [{'doc_id':    {'data_type': 'int'}},
                                  {'username':  {'data_type': 'string'}}],
                                 [{'role_code': {'data_type': 'string'}},
                                  {'email':     {'data_type': 'string'}},
                                  {'active':    {'data_type': 'bool'}},
                                  {'created':   {'data_type': 'created'}},
                                  {'updated':   {'data_type': 'updated'}}],
                                 [])

class DocUser(DataObject):
    """
    An association between a document and a user.
    """

docusers = DocUsers()
docusers.load()

