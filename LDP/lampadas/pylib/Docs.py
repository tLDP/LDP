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
                 
    def load(self):
        DataCollection.load(self)
        self.languages = LampadasCollection()
        for key in self.keys():
            doc = self[key]
            self.adjust_lang_count(doc.lang, 1)
            doc.errors.doc_id   = doc.id
            doc.files.doc_id    = doc.id
            doc.users.doc_id    = doc.id
            doc.versions.doc_id = doc.id
            doc.ratings.doc_id  = doc.id
            doc.notes.doc_id    = doc.id
        self.load_errors()
        self.load_users()
        self.load_docfiles()
        self.load_versions()
        self.load_ratings()
        self.load_topics()
        self.load_collections()
        self.load_notes()

    def load_errors(self):
        sql = "SELECT doc_id, err_id, created, notes FROM document_error"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doc_id = row[0]
            doc = self[doc_id]
            docerr = DocErr()
            docerr.load_row(row)
            doc.errors[docerr.err_id] = docerr

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


    def load_docfiles(self):
        sql = "SELECT doc_id, filename, top FROM document_file"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doc_id = row[0]
            doc = self[doc_id]
            docfile = DocFile()
            docfile.load_row(row)
            doc.files[docfile.filename] = docfile
        for doc_id in self.keys():
            self[doc_id].files.count_errors()


    def load_versions(self):
        sql = "SELECT doc_id, rev_id, version, pub_date, initials, notes FROM document_rev"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doc_id = row[0]
            doc = self[doc_id]
            docversion = DocVersion()
            docversion.load_row(row)
            doc.versions[docversion.id] = docversion

    def load_ratings(self):
        sql = "SELECT doc_id, username, created, vote FROM doc_vote"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doc_id = row[0]
            doc = self[doc_id]
            doc.ratings.parent = doc
            docrating = DocRating()
            docrating.load_row(row)
            doc.ratings[docrating.username] = docrating

    def load_topics(self):
        for key in self.keys():
            doc = self[key]
            doc.topics = doctopics.apply_filter(DocTopics, Filter('doc_id', '=', doc.id))

    def load_collections(self):
        sql = "SELECT doc_id, collection_code FROM document_collection"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doc_id = row[0]
            doc = self[doc_id]
            doccollection = DocCollection()
            doccollection.load_row(row)
            doc.collections[doccollection.collection_code] = doccollection

    def load_notes(self):
        sql = 'SELECT note_id, doc_id, notes, creator, created FROM notes'
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doc_id = row[1]
            doc = self[doc_id]
            docnote = DocNote()
            docnote.load_row(row)
            doc.notes[docnote.id] = docnote

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
        self.errors                  = DocErrs()
        self.errors.doc_id           = self.id
        self.files                   = DocFiles()
        self.files.doc_id            = self.id
        self.users                   = DocUsers()
        self.users.doc_id            = self.id
        self.versions                = DocVersions()
        self.versions.doc_id         = self.id
        self.ratings                 = DocRatings()
        self.ratings.doc_id          = self.id
        self.ratings.parent          = self.id
        self.collections             = DocCollections()
        self.collections.doc_id      = self.id
        self.notes                   = DocNotes()
        self.notes.doc_id            = self.id

    def load(self):
        DataObject.load(self)
        self.topics                  = doctopics.apply_filter(DocTopics, Filter('doc_id', '=', self.id))
        self.errors                  = DocErrs(self.id)
        self.files                   = DocFiles(self.id)
        self.users                   = DocUsers(self.id)
        self.versions                = DocVersions(self.id)
        self.ratings                 = DocRatings(self.id)
        self.ratings.parent          = self
        self.collections             = DocCollections(self.id)
        self.notes                   = DocNotes(self.id)

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

# DocErrs

class DocErrs(LampadasCollection):
    """
    A collection object providing access to all document errors, as identified by the
    Lintadas subsystem.
    """

    def __init__(self, doc_id=0):
        self.data = {}
        self.doc_id = doc_id
        if doc_id > 0:
            self.load()

    def load(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT doc_id, err_id, notes, created FROM document_error WHERE doc_id=" + str(self.doc_id)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doc_err = DocErr()
            doc_err.load_row(row)
            self.data[doc_err.err_id] = doc_err

    def count(self, err_type_code=None):
        if err_type_code==None:
            return len(self)
        else:
            i = 0
            for key in self.keys():
                print key
                print self.keys()
                docerror = self[key]
                error = errors[docerror.err_id]
                if errors[key].err_type_code==err_type_code:
                    i = i + 1
            return i
        
    def clear(self, err_type_code=None):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sqlbase = "DELETE FROM document_error WHERE doc_id=" + str(self.doc_id)
        if err_type_code==None:
            db.runsql(sqlbase)
            self.data = {}
        else:
            errortype = errortypes[err_type_code]
            for key in errors.keys():
                error = errors[key]
                if error.err_type_code==err_type_code:
                    sql = sqlbase + ' AND err_id=' + str(error.id)
                    db.runsql(sql)
                    if self[error.id]:
                        del self[error.id]
        db.commit()

# FIXME: Try instantiating a DocErr object, then adding it to the *document*
# rather than passing all these parameters here. --nico

    def add(self, doc_id, err_id, notes=''):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "INSERT INTO document_error(doc_id, err_id, notes) VALUES (" + str(doc_id) + ", " + str(err_id) + ', ' + wsq(notes) + ')'
        assert db.runsql(sql)==1
        doc_err = DocErr()
        doc_err.doc_id = doc_id
        doc_err.err_id = err_id
        doc_err.created = now_string()
        doc_err.notes = notes
        self[doc_err.err_id] = doc_err
        db.commit()

class DocErr:
    """
    An error filed against a document by the Lintadas subsystem.
    """

    def load_row(self, row):
        self.doc_id	 = safeint(row[0])
        self.err_id  = safeint(row[1])
        self.notes   = trim(row[2])
        self.created = time2str(row[3])


# DocFiles

class DocFiles(LampadasCollection):
    """
    A collection object providing access to all document source files.
    """

    def __init__(self, doc_id=0):
        self.data = {}
        self.doc_id = doc_id
        if doc_id > 0:
            self.load()

    def load(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT doc_id, filename, top FROM document_file WHERE doc_id=" + str(self.doc_id)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            docfile = DocFile()
            docfile.load_row(row)
            self.data[docfile.filename] = docfile
        self.count_errors()

    def add(self, doc_id, filename, top):
        # First, add a sourcefile record if it doesn't exist
        sourcefile = sourcefiles[filename]
        if sourcefile==None:
            sourcefiles.add(filename)

        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = 'INSERT INTO document_file (doc_id, filename, top) VALUES (' + str(doc_id) + ', ' + wsq(filename) + ', ' + wsq(bool2tf(top)) + ')'
        assert db.runsql(sql)==1
        db.commit()
        file = DocFile()
        file.doc_id = doc_id
        file.filename = filename
        file.top = top
        file.save()
        self.data[file.filename] = file
        return file
        
    def delete(self, filename):
        file = self[filename]
        sql = "DELETE FROM document_file WHERE doc_id=" + str(self.doc_id) + " AND filename=" + wsq(filename)
        db.runsql(sql)
        db.commit()
        del self.data[filename]
        
    def save(self):
        for key in self.keys():
            self[key].save()
        
    def clear(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "DELETE FROM document_file WHERE doc_id=" + str(self.doc_id)
        db.runsql(sql)
        db.commit()
        self.data = {}

    def count_errors(self):
        self.error_count = 0
        for key in self.keys():
            sourcefile = sourcefiles[key]
            self.error_count = self.error_count + sourcefile.errors.count()

class DocFile:
    """
    An association between a document and a file.
    """

    def __init__(self, filename=''):
        self.filename = filename
        if filename=='': return
        self.load()

    def load(self):
        sql = 'SELECT doc_id, filename, top FROM document_file WHERE doc_id=' + str(self.doc_id) + ' AND filename=' + wsq(self.filename)
        cursor = db.select(sql)
        row = cursor.fetchone()
        if row==None: return
        self.load_row(row)
    
    def load_row(self, row):
        self.doc_id      = row[0]
        self.filename    = trim(row[1])
        self.top         = tf2bool(row[2]) 
        
    def save(self):
        # FIXME -- trying to start replacing wsq(), etc. --nico 
        #sql = 'UPDATE document_file SET top=' + wsq(bool2tf(self.top)) + ', format_code=' + wsq(self.format_code) + ' WHERE doc_id='+ str(self.doc_id) + ' AND filename='+ wsq(self.filename)
        #db.runsql(sql)
        dict = {'doc_id':self.doc_id,
                'filename':self.filename,
                'top':bool2tf(self.top)}
        sql = sqlgen.update('document_file',dict,['doc_id','filename'])
        db.execute(sql,dict)
        db.commit()


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


# DocRatings

class DocRatings(LampadasCollection):
    """
    A collection object providing access to all ratings placed on documents by users.
    """

    def __init__(self, doc_id=0):
        self.data = {}
        self.doc_id = doc_id
        if doc_id > 0:
            self.load()

    def load(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT doc_id, username, created, vote FROM doc_vote WHERE doc_id=" + str(self.doc_id)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            docrating = DocRating()
            docrating.load_row(row)
            self.doc_id = docrating.doc_id
            self.data[docrating.username] = docrating

    def add(self, username, rating):
        docrating = DocRating()
        docrating.doc_id   = self.doc_id
        docrating.username = username
        docrating.created  = now_string()
        docrating.rating   = rating
        docrating.save()
        self.data[docrating.username] = docrating

    def delete(self, username):
        if self.data[username]==None: return
        del self.data[username]
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = 'DELETE FROM doc_vote WHERE doc_id=' + str(self.doc_id) + ' AND username=' + wsq(username)
        db.runsql(sql)
        
    def clear(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "DELETE FROM doc_vote WHERE doc_id=" + str(self.doc_id)
        db.runsql(sql)
        self.data = {}

class DocRating:
    """
    A rating of a document, assigned by a registered user.
    """

    def load_row(self, row):
        assert not row==None
        self.doc_id   = row[0]
        self.username = row[1]
        self.created  = time2str(row[2])
        self.rating   = row[3]

    def save(self):
        """
        FIXME: use cursor.execute(sql,params) instead! --nico
        """
        sql = "DELETE from doc_vote WHERE doc_id=" + str(self.doc_id) + " AND username=" + wsq(self.username)
        db.runsql(sql)
        sql = "INSERT INTO doc_vote (doc_id, username, vote) VALUES (" + str(self.doc_id) + ", " + wsq(self.username) + ", " + str(self.rating) + ")"
        db.runsql(sql)
        db.commit()


# DocVersions

class DocVersions(LampadasCollection):
    """
    A collection object providing access to document revisions.
    """

    def __init__(self, doc_id=0):
        LampadasCollection.__init__(self)
        self.doc_id = doc_id
        if doc_id > 0:
            self.load()

    def load(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT doc_id, rev_id, version, pub_date, initials, notes FROM document_rev WHERE doc_id=" + str(self.doc_id)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            docversion = DocVersion()
            docversion.load_row(row)
            self.data[docversion.id] = docversion

    def add(self, version, pub_date, initials, notes):
        newrev_id = db.next_id('document_rev', 'rev_id')
        sql = 'INSERT INTO document_rev(doc_id, rev_id, version, pub_date, initials, notes) VALUES (' + str(self.doc_id) + ', ' + str(newrev_id) + ', ' + wsq(version) + ', ' + wsq(pub_date) + ', ' + wsq(initials) + ', ' + wsq(notes) + ')'
        db.runsql(sql)
        db.commit()
        docversion = DocVersion()
        docversion.id = newrev_id
        docversion.doc_id = self.doc_id
        docversion.version = version
        docversion.pub_date = pub_date
        docversion.initials = initials
        docversion.notes = notes
        self.data[docversion.id] = docversion

    def delete(self, rev_id):
        sql = 'DELETE FROM document_rev WHERE rev_id=' + str(rev_id)
        db.runsql(sql)
        db.commit()
        del self.data[rev_id]

    def clear(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "DELETE FROM document_rev WHERE doc_id=" + str(self.doc_id)
        db.runsql(sql)
        db.commit()
        self.data = {}

class DocVersion:
    """
    A release of the document.
    """

    def load_row(self, row):
        self.doc_id   = row[0]
        self.id       = row[1]
        self.version  = trim(row[2])
        self.pub_date = date2str(row[3])
        self.initials = trim(row[4])
        self.notes    = trim(row[5])

    def save(self):
        """
        FIXME: use cursor.execute(sql,params) instead! --nico
        """
        sql = "UPDATE document_rev SET version=" + wsq(self.version) + ", pub_date=" + wsq(self.pub_date) + ", initials=" + wsq(self.initials) + ", notes=" + wsq(self.notes) + "WHERE doc_id=" + str(self.doc_id) + " AND rev_id=" + str(self.id)
        assert db.runsql(sql)==1
        db.commit()


# DocCollections

class DocCollections(LampadasCollection):
    """
    A collection object providing access to document collections.
    """

    def __init__(self, doc_id=0):
        LampadasCollection.__init__(self)
        self.doc_id = doc_id
        if doc_id > 0:
            self.load()

    def load(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT doc_id, collection_code FROM document_collection WHERE doc_id=" + str(self.doc_id)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doccollection = DocCollection()
            doccollection.load_row(row)
            self.data[doccollection.collection_code] = doccollection

    def add(self, collection_code):
        sql = 'INSERT INTO document_collection(doc_id, collection_code) VALUES (' + str(self.doc_id) + ', ' + wsq(collection_code) + ')'
        db.runsql(sql)
        db.commit()
        doccollection = DocCollection()
        doccollection.doc_id = self.doc_id
        doccollection.collection_code = collection_code
        self.data[doccollection.collection_code] = doccollection

    def delete(self, collection_code):
        sql = 'DELETE FROM document_collection WHERE doc_id=' + str(self.doc_id) + ' AND collection_code=' + wsq(collection_code)
        db.runsql(sql)
        db.commit()
        del self.data[collection_code]

    def clear(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "DELETE FROM document_collection WHERE doc_id=" + str(self.doc_id)
        db.runsql(sql)
        db.commit()
        self.data = {}

class DocCollection:
    """
    A collection for the document.
    """

    def load_row(self, row):
        self.doc_id   = row[0]
        self.collection_code  = trim(row[1])


# DocNotes

class DocNotes(LampadasCollection):
    """
    A collection object providing access to document notes.
    """

    def __init__(self, doc_id=0):
        self.data = {}
        self.doc_id = doc_id
        if doc_id > 0:
            self.load()

    def load(self):
        self.data = {}
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = 'SELECT note_id, doc_id, notes, creator, created FROM notes WHERE doc_id=' + str(self.doc_id)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            docnote = DocNote()
            docnote.load_row(row)
            self[docnote.id] = docnote

    def add(self, notes, creator):
        note_id = db.next_id('notes', 'note_id')
        sql = 'INSERT INTO notes(note_id, doc_id, notes, creator) VALUES (' + str(note_id) + ', ' + str(self.doc_id) + ', ' + wsq(notes) + ', ' + wsq(creator) + ')'
        db.runsql(sql)
        db.commit()
        docnote = DocNote()
        docnote.id      = note_id
        docnote.doc_id  = self.doc_id
        docnote.created = now_string()
        docnote.notes   = notes
        docnote.creator = creator
        self.data[docnote.id] = docnote

    def delete(self, note_id):
        sql = 'DELETE FROM notes WHERE note_id=' + str(note_id) 
        db.runsql(sql)
        db.commit()
        del self.data[note_id]

    def clear(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "DELETE FROM notes WHERE doc_id=" + str(self.doc_id)
        db.runsql(sql)
        db.commit()
        self.data = {}

class DocNote:
    """
    A note for the document.
    """

    def load_row(self, row):
        self.id      = row[0]
        self.doc_id  = row[1]
        self.notes   = trim(row[2])
        self.creator = trim(row[3])
        self.created = time2str(row[4])

docs = Docs()
docs.load()
