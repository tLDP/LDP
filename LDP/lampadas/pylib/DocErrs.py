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
from Errors import errors

class DocErrs(DataCollection):
    """
    A collection object providing access to all document errors, as identified by the
    Lintadas subsystem.
    """

    def __init__(self):
        DataCollection.__init__(self, None, DocErr,
                                 'document_error',
                                 [{'err_id':  {'data_type': 'int'}},
                                  {'doc_id':  {'data_type': 'int'}}],
                                 [{'notes':   {'data_type': 'string'}},
                                  {'created': {'data_type': 'created'}},
                                  {'updated': {'data_type': 'updated'}}],
                                 [])
    
    def count(self, err_type_code=None):
        if err_type_code==None:
            return DataCollection.count(self)
        else:
            i = 0
            for key in self.keys():
                object = self[key]
                error = errors[object.err_id]
                if error.err_type_code==err_type_code:
                    i = i + 1
            return i
        
    def clear(self, err_type_code=None):
        if err_type_code==None:
            DataCollection.clear(self)
        else:
            for key in self.keys():
                object = self[key]
                error = errors[object.err_id]
                if error.err_type_code==err_type_code:
                    object.delete()
        self.refresh_filters()

class DocErr(DataObject):
    """
    An error filed against a document by the Lintadas subsystem.
    """
    pass

docerrs = DocErrs()
docerrs.load()

