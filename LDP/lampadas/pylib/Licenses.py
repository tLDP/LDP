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

# Licenses

class Licenses(DataCollection):
    """
    A collection object of all licenses.
    """
    
    def __init__(self):
        DataCollection.__init__(self, None, License,
                                 'license',
                                 {'license_code':        {'data_type': 'string', 'attribute': 'code'}},
                                 [{'free':               {'data_type': 'bool'}},
                                  {'dfsg_free':          {'data_type': 'bool'}},
                                  {'osi_cert_free':      {'data_type': 'bool'}},
                                  {'url':                {'data_type': 'string'}},
                                  {'sort_order':         {'data_type': 'int'}}],
                                 [{'license_short_name': {'data_type': 'string', 'attribute': 'short_name'}},
                                  {'license_name':       {'data_type': 'string', 'attribute': 'name'}},
                                  {'license_desc':       {'data_type': 'string', 'attribute': 'description'}}])

class License(DataObject):
    """
    A documentation or software license.
    """
    pass

licenses = Licenses()
licenses.load()
