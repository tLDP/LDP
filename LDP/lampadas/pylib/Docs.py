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
                               {'doc_id':                   {'data_type': 'int',    'attribute': 'id'}},
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
                                {'rating':                  {'data_type': 'int',    'nullable': 1}},
                                {'lang':                    {'data_type': 'string'}},
                                {'sk_seriesid':             {'data_type': 'string'}},
                                {'replaced_by_id':          {'data_type': 'int',    'nullable': 1}},
                                {'lint_time':               {'data_type': 'time'}},
                                {'pub_time':                {'data_type': 'time'}},
                                {'mirror_time':             {'data_type': 'time'}},
                                {'first_pub_date':          {'data_type': 'date'}}],
                               [])
                 
    def load(self, updated=''):
        DataCollection.load(self, updated)
        self.languages = LampadasCollection()
        for key in self.keys():
            doc = self[key]
            if updated=='':
                self.adjust_lang_count(doc.lang, 1)
                doc.users.doc_id = doc.id
                doc.topics.refresh_filters()
                doc.errors.refresh_filters()
                doc.files.refresh_filters()
                doc.versions.refresh_filters()
                doc.ratings.refresh_filters()
                doc.collections.refresh_filters()
                doc.notes.refresh_filters()
        self.load_users()

    def load_users(self):
        sql = "SELECT doc_id, username, role_code, email, active FROM document_user"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doc_id = row[0]
            doc = self[doc_id]
            docuser = DocUser()
            docuser.load_row(row)
            doc.users[docuser.username] = docuser


    def adjust_lang_count(self, lang_code, delta):
        """
        Increment or decrement the document count for a language.
        """
        if self.languages[lang_code]==None:
            self.languages[lang_code] = 0
        self.languages[lang_code] = self.languages[lang_code] + delta

# FIXME: try instantiating a new document, then adding *it* to the collection,
# rather than passing in all these parameters. --nico

    def add(self, title, short_title, type_code, format_code, dtd_code, dtd_version, version, last_update, isbn, encoding, pub_status_code, review_status_code, tickle_date, pub_date, tech_review_status_code, license_code, license_version, copyright_holder, abstract, short_desc, lang, sk_seriesid, replaced_by_id, lint_time, pub_time, mirror_time, first_pub_date):

        # FIXME: Make this a property of the DataCollection class
        
        id = db.next_id('document', 'doc_id')
        
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "INSERT INTO document(doc_id, title, short_title, type_code, format_code, dtd_code, dtd_version, version, last_update, isbn, encoding, pub_status_code, review_status_code, tickle_date, pub_date, tech_review_status_code, license_code, license_version, copyright_holder, abstract, short_desc, lang, sk_seriesid, replaced_by_id, lint_time, pub_time, mirror_time, first_pub_date) VALUES (" + str(id) + ", " + wsq(title) + ", " + wsq(short_title) + ', ' + wsq(type_code) + ", " + wsq(format_code) + ", " + wsq(dtd_code) + ", " + wsq(dtd_version) + ", " + wsq(version) + ", " + wsq(last_update) + ", " + wsq(isbn) + ", " + wsq(encoding) + ', ' +  wsq(pub_status_code) + ", " + wsq(review_status_code) + ", " + wsq(tickle_date) + ", " + wsq(pub_date) + ", " + wsq(tech_review_status_code) + ", " + wsq(license_code) + ", " + wsq(license_version) + ', ' + wsq(copyright_holder) + ', ' + wsq(abstract) + ", " + wsq(short_desc) + ', ' + wsq(lang) + ", " + wsq(sk_seriesid) + ', ' + str(replaced_by_id) + ', ' + wsq(lint_time) + ', ' + wsq(pub_time) + ', ' + wsq(mirror_time) + ', ' + wsq(first_pub_date) + ')'
        assert db.runsql(sql)==1
        db.commit()
        doc = Doc(self)
        doc.id = id
        doc.load()
        self[doc.id] = doc
        self.adjust_lang_count(doc.lang, 1)
        return doc
    
    def delete(self, id):
        # FIXME: use cursor.execute(sql,params) instead! --nico

        doc = self[id]
        if doc==None:
            return

        # Delete dependent data first!
        doc.errors.clear()
        doc.files.clear()
        doc.users.clear()
        doc.versions.clear()
        doc.ratings.clear()
        doc.topics.clear()
        doc.notes.clear()
        doc.collections.clear()
        self.adjust_lang_count(doc.lang, -1)

        sql = ('DELETE from document WHERE doc_id=' + str(id))
        assert db.runsql(sql)==1
        db.commit()
        del self[id]

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
        self.id                      = 0
        self.title                   = ''
        self.short_title             = ''
        self.type_code               = ''
        self.format_code             = ''
        self.dtd_code                = ''
        self.dtd_version             = ''
        self.version                 = ''
        self.last_update             = ''
        self.isbn                    = ''
        self.encoding                = ''
        self.pub_status_code         = ''
        self.review_status_code      = ''
        self.tickle_date             = ''
        self.pub_date                = ''
        self.tech_review_status_code = ''
        self.maintained              = 0
        self.maintainer_wanted       = ''
        self.license_code            = ''
        self.license_version         = ''
        self.copyright_holder        = ''
        self.abstract                = ''
        self.short_desc              = ''
        self.rating                  = 0
        self.lang                    = ''
        self.sk_seriesid             = ''
        self.replaced_by_id          = 0
        self.lint_time               = ''
        self.pub_time                = ''
        self.mirror_time             = ''
        self.first_pub_date          = ''
        self.users                   = DocUsers()
        self.users.doc_id            = self.id
        self.topics = doctopics.apply_filter(DocTopics, Filter(self, 'id', '=', 'doc_id'))
        self.errors = docerrs.apply_filter(DocErrs, Filter(self, 'id', '=', 'doc_id'))
        self.files = docfiles.apply_filter(DocFiles, Filter(self, 'id', '=', 'doc_id'))
        self.versions = docversions.apply_filter(DocVersions, Filter(self, 'id', '=', 'doc_id'))
        self.ratings = docratings.apply_filter(DocRatings, Filter(self, 'id', '=', 'doc_id'))
        self.collections = doccollections.apply_filter(DocCollections, Filter(self, 'id', '=', 'doc_id'))
        self.notes = docnotes.apply_filter(DocNotes, Filter(self, 'id', '=', 'doc_id'))

    def load(self):
        DataObject.load(self)
        self.users = DocUsers(self.id)
        self.topics.refresh_filters()
        self.errors.refresh_filters()
        self.files.refresh_filters()
        self.versions.refresh_filters()
        self.ratings.refresh_filters()
        self.collections.refresh_filters()
        self.notes.refresh_filters()

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
        self.calc_rating()
        DataObject.save(self)

    def calc_rating(self):
        self.rating = 0
        count = 0
        if self.ratings.count() > 0:
            keys = self.ratings.keys()
            for key in keys:
                self.rating = self.rating + self.ratings[key].rating
                count = count + 1
            self.rating = self.rating / count

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

# DocUsers

class DocUsers(LampadasCollection):
    """
    A collection object providing access to all document volunteers.
    """

    def __init__(self, doc_id=0):
        self.data = {}
        self.doc_id = doc_id
        if doc_id > 0:
            self.load()

    def load(self):
        sql = "SELECT doc_id, username, role_code, email, active FROM document_user WHERE doc_id=" + str(self.doc_id)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            docuser = DocUser()
            docuser.load_row(row)
            self.data[docuser.username] = docuser

    def add(self, username, role_code='author', email='', active=1):
        sql = 'INSERT INTO document_user (doc_id, username, role_code, email, active) VALUES (' + str(self.doc_id) + ', ' + wsq(username) + ', ' + wsq(role_code) + ', ' + wsq(email) + ', ' + wsq(bool2tf(active)) + ')'
        db.runsql(sql)
        db.commit()
        docuser = DocUser()
        docuser.doc_id = self.doc_id
        docuser.username = username
        docuser.role_code = role_code
        docuser.email = email
        docuser.active = active
        self.data[docuser.username] = docuser

    def delete(self, username):
        sql = 'DELETE FROM document_user WHERE doc_id=' + str(self.doc_id) + ' AND username=' + wsq(username)
        db.runsql(sql)
        db.commit()
        del self.data[username]
        
    def clear(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "DELETE FROM document_user WHERE doc_id=" + str(self.doc_id)
        db.runsql(sql)
        db.commit()
        self.data = {}

class DocUser:
    """
    An association between a document and a user.
    """

    def load_row(self, row):
        self.doc_id    = row[0]
        self.username  = trim(row[1])
        self.role_code = trim(row[2]) 
        self.email     = trim(row[3])
        self.active    = tf2bool(row[4])
        
    def save(self):
        """
        FIXME: use cursor.execute(sql,params) instead! --nico
        """
        sql = 'UPDATE document_user SET role_code=' + wsq(self.role_code) + ', email=' + wsq(self.email) + ', active=' + wsq(bool2tf(self.active)) + ' WHERE doc_id='+ str(self.doc_id) + ' AND username='+ wsq(self.username)
        db.runsql(sql)
        db.commit()

    def delete(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "DELETE FROM document_user WHERE doc_id=" + str(self.doc_id) + " AND username=" + wsq(self.username)
        db.runsql(sql)
        db.commit()

docs = Docs()
docs.load()
