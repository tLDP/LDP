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

class DocNotes(DataCollection):
    """
    A collection object providing access to document notes.
    """

    def __init__(self, doc_id=0):
        DataCollection.__init__(self, None, DocNote,
                                 'document_notes',
                                 {'note_id':  {'data_type': 'sequence'}},
                                 [{'doc_id':  {'data_type': 'int'}},
                                  {'notes':   {'data_type': 'string'}},
                                  {'creator': {'data_type': 'creator'}},
                                  {'created': {'data_type': 'created'}},
                                  {'updated': {'data_type': 'updated'}}],
                                 [])

class DocNote(DataObject):
    """
    A note for the document.
    """
    pass

docnotes = DocNotes()
docnotes.load()

