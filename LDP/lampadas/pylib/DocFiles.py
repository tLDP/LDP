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
# DocFiles

from BaseClasses import *
from SourceFiles import sourcefiles

class DocFiles(DataCollection):
    """
    A collection object providing access to all document source files.
    """

    def __init__(self):
        DataCollection.__init__(self, None, DocFile,
                                 'document_file',
                                 [{'doc_id':   {'data_type': 'int'}},
                                  {'filename': {'data_type': 'string'}}],
                                  [{'top':     {'data_type': 'bool'}},
                                  {'created':  {'data_type': 'created'}},
                                  {'updated':  {'data_type': 'updated'}}],
                                 [])

    def add(self, docfile):
        if sourcefiles[docfile.filename]==None:
            sourcefiles.add(docfile.filename)
        DataCollection.add(self, docfile)
            
    def error_count(self):
        count = 0
        for key in self.keys():
            filename = self[key].filename
            sourcefile = sourcefiles[filename]
            count = count + sourcefile.errors.count()
        return count

class DocFile(DataObject):
    """
    An association between a document and a file.
    """
    pass

docfiles = DocFiles()
docfiles.load()

