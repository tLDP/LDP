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

# ReviewStatuses

class ReviewStatuses(DataCollection):
    """
    A collection object of all publication statuses.
    """
    
    def __init__(self):
        DataCollection.__init__(self, ReviewStatus,
                                 'review_status',
                                 {'review_status_code':  {'data_type': 'string', 'attribute': 'code'}},
                                 {'sort_order':          {'data_type': 'int'}},
                                 [{'review_status_name': {'data_type': 'string', 'attribute': 'name'}},
                                  {'review_status_desc': {'data_type': 'string', 'attribute': 'description'}}])

class ReviewStatus(DataObject):
    """
    The Review Status defines where in the review process a
    document is.
    """
    pass

review_statuses = ReviewStatuses()
review_statuses.load()
