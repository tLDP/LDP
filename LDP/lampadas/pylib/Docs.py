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
# Collections

from Globals import *
from BaseClasses import *
from DocUsers import docusers, DocUsers
from DocTopics import doctopics, DocTopics
from DocErrs import docerrs, DocErrs
from DocFiles import docfiles, DocFiles
from DocVersions import docversions, DocVersions
from DocRatings import docratings, DocRatings
from DocCollections import doccollections, DocCollections
from DocNotes import docnotes, DocNotes

from SourceFiles import sourcefiles
from ErrorTypes import errortypes
from Errors import errors
from sqlgen import sqlgen


# Documents

class Docs(DataCollection):
    """
    A collection object providing access to all documents.
    """

    def __init__(self):
        DataCollection.__init__(self, None, Doc,
                               'document',
                               {'doc_id':                   {'data_type': 'sequence', 'attribute': 'id'}},
                               [{'title':                   {'data_type': 'string'}},
                                {'short_title':             {'data_type': 'string'}},
                                {'type_code':               {'data_type': 'string'}}, 
                                {'format_code':             {'data_type': 'string'}}, 
                                {'dtd_code':                {'data_type': 'string'}}, 
                                {'dtd_version':             {'data_type': 'string'}},
                                {'version':                 {'data_type': 'string'}}, 
                                {'last_update':             {'data_type': 'date'}}, 
                                {'isbn':                    {'data_type': 'string'}}, 
                                {'encoding':                {'data_type': 'string'}}, 
                                {'pub_status_code':         {'data_type': 'string'}}, 
                                {'review_status_code':      {'data_type': 'string'}},
                                {'tickle_date':             {'data_type': 'date'}}, 
                                {'pub_date':                {'data_type': 'date'}}, 
                                {'tech_review_status_code': {'data_type': 'string'}},
                                {'maintained':              {'data_type': 'bool'}},
                                {'maintainer_wanted':       {'data_type': 'bool'}},
                                {'license_code':            {'data_type': 'string'}},
                                {'license_version':         {'data_type': 'string'}}, 
                                {'copyright_holder':        {'data_type': 'string'}}, 
                                {'abstract':                {'data_type': 'string'}}, 
                                {'short_desc':              {'data_type': 'string'}},
                                {'rating':                  {'data_type': 'int',      'nullable': 1}},
                                {'lang':                    {'data_type': 'string'}},
                                {'sk_seriesid':             {'data_type': 'string',   'nullable': 0}},
                                {'replaced_by_id':          {'data_type': 'int',      'nullable': 1}},
                                {'lint_time':               {'data_type': 'time'}},
                                {'pub_time':                {'data_type': 'time'}},
                                {'mirror_time':             {'data_type': 'time'}},
                                {'first_pub_date':          {'data_type': 'date'}}],
                               [])
                 
    
    def sort_by_metadata(self, attribute):
        temp, result = [], []
        for key, item in self.items():
            metadata = item.metadata()
            value = getattr(metadata, attribute)
            temp.append((value, key))
        temp.sort()
        for v,k in temp :
            result.append(k)
        return result
        
class Doc(DataObject):
    """
    A document in any format, whether local or remote.
    """

    def __init__(self, parent):
        DataObject.__init__(self, parent)
        DataObject.add_child(self, 'users',       docusers.apply_filter(DocUsers, Filter(self, 'id', '=', 'doc_id')))
        DataObject.add_child(self, 'topics',      doctopics.apply_filter(DocTopics, Filter(self, 'id', '=', 'doc_id')))
        DataObject.add_child(self, 'errors',      docerrs.apply_filter(DocErrs, Filter(self, 'id', '=', 'doc_id')))
        DataObject.add_child(self, 'files',       docfiles.apply_filter(DocFiles, Filter(self, 'id', '=', 'doc_id')))
        DataObject.add_child(self, 'versions',    docversions.apply_filter(DocVersions, Filter(self, 'id', '=', 'doc_id')))
        DataObject.add_child(self, 'ratings',     docratings.apply_filter(DocRatings, Filter(self, 'id', '=', 'doc_id')))
        DataObject.add_child(self, 'collections', doccollections.apply_filter(DocCollections, Filter(self, 'id', '=', 'doc_id')))
        DataObject.add_child(self, 'notes',       docnotes.apply_filter(DocNotes, Filter(self, 'id', '=', 'doc_id')))

    def remove_duplicate_metadata(self):
        # FIXME: This is temporary code to get rid of redundant
        # stuff. Once we have good, clean data we can 
        # discard it.

        # If our metadata matches that of our top file, it is
        # redundant, so discard it.
        topfile = self.find_top_file()
        if topfile:
            sourcefile = sourcefiles[topfile.filename]
            updated = 0
            if string_match(self.format_code, sourcefile.format_code)==1:
                self.format_code = ''
                updated = 1
            if string_match(self.dtd_code, sourcefile.dtd_code)==1:
                self.dtd_code = ''
                updated = 1
            if string_match(self.dtd_version, sourcefile.dtd_version)==1:
                self.dtd_version = ''
                updated = 1
            if string_match(self.title, sourcefile.title)==1:
                self.title = ''
                updated = 1
            if string_match(self.abstract, sourcefile.abstract)==1:
                self.abstract = ''
                updated = 1
            if string_match(self.version, sourcefile.version)==1:
                self.version = ''
                updated = 1
            if string_match(self.pub_date, sourcefile.pub_date)==1:
                self.pub_date = ''
                updated = 1
            if string_match(self.isbn, sourcefile.isbn)==1:
                self.isbn = ''
                updated = 1
            if string_match(self.encoding, sourcefile.encoding)==1:
                self.encoding = ''
                updated = 1
            if updated==1:
                self.save()

    def save(self):
        """
        FIXME: use cursor.execute(sql,params) instead! --nico
        """

        # Discard superfluous meta-data
        docfile = self.find_top_file()
        if docfile:
            sourcefile = sourcefiles[docfile.filename]
            if string_match(self.format_code, sourcefile.format_code)==1:
                self.format_code = ''
            if string_match(self.dtd_code, sourcefile.dtd_code)==1:
                self.dtd_code = ''
            if string_match(self.dtd_version, sourcefile.dtd_version)==1:
                self.dtd_version = ''
            if string_match(self.title, sourcefile.title)==1:
                self.title = ''
            if string_match(self.abstract, sourcefile.abstract)==1:
                self.abstract = ''
            if string_match(self.version, sourcefile.version)==1:
                self.version = ''
            if string_match(self.pub_date, sourcefile.pub_date)==1:
                self.pub_date = ''
            if string_match(self.isbn, sourcefile.isbn)==1:
                self.isbn = ''
            if string_match(self.encoding, sourcefile.encoding)==1:
                self.encoding = ''
        
        # Always recalculate the rating when saving a document.
        DataObject.save(self)

    def find_top_file(self):
        for filename in self.files.keys():
            docfile = self.files[filename]
            if docfile.top==1:
                return docfile

    def metadata(self):
        temp = DocMetaData()
        temp.format_code = self.format_code
        temp.dtd_code    = self.dtd_code
        temp.dtd_version = self.dtd_version
        temp.title       = self.title
        temp.abstract    = self.abstract
        temp.version     = self.version
        temp.pub_date    = self.pub_date
        temp.isbn        = self.isbn
        temp.encoding    = self.encoding
        docfile = self.find_top_file()
        if docfile:
            sourcefile = sourcefiles[docfile.filename]
            if temp.format_code=='': temp.format_code = sourcefile.format_code
            if temp.dtd_code=='':    temp.dtd_code    = sourcefile.dtd_code
            if temp.dtd_version=='': temp.dtd_version = sourcefile.dtd_version
            if temp.title=='':       temp.title       = sourcefile.title
            if temp.abstract=='':    temp.abstract    = sourcefile.abstract
            if temp.version=='':     temp.version     = sourcefile.version
            if temp.pub_date=='':    temp.pub_date    = sourcefile.pub_date
            if temp.isbn=='':        temp.isbn        = sourcefile.isbn
            if temp.encoding=='':    temp.encoding    = sourcefile.encoding
        return temp
       
# DocMetaData

class DocMetaData:

    def __init__(self):
        self.doc_id      = 0
        self.format_code = ''
        self.dtd_code    = ''
        self.dtd_version = ''
        self.title       = ''
        self.abstract    = ''
        self.version     = ''
        self.pub_date    = ''
        self.isbn        = ''
        self.encoding    = ''

docs = Docs()
docs.load()
