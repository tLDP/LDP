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
"""
Lampadas Object Hierarchy Module

This module defines Data Objects (Users, Docs, Notes, Topics, etc.)
for the Lampadas system. All access to the underlying database should be
performed through this layer.
"""

# Modules

# FIXME import * is considered evil for you can pollute your namespace if
# the imported module changes or makes a mistake --nico

from Globals import *
from Config import config
from Database import db
from Log import log
from BaseClasses import *
from SourceFiles import sourcefiles
from Languages import languages
import string
import os.path

from sqlgen import sqlgen

# Lampadas

class Lampadas:
    """
    This is the top level container class for all Lampadas objects.
    While you can also create User, Doc, and other classes independently,
    this class can be instantiated and all those objects accessed as part
    of a single object hierarchy.

    Using this method gives you complete data caching capabilities and a
    single, global access route to all Lampadas data.
    """
    
    def __init__(self):
        self.load()

    def user(self, username):
        return User(username)

    def load(self):
        log(3, 'Loading Lampadas data')
        self.types           = Types()
        self.types.load()
        self.docs            = Docs()
        self.docs.load()
        self.roles           = Roles()
        self.roles.load()
        self.licenses        = Licenses()
        self.licenses.load()
        self.dtds            = DTDs()
        self.dtds.load()
        self.errors          = Errors()
        self.errors.load()
        self.formats         = Formats()
        self.formats.load()
        self.languages       = languages
        self.languages.load()
        self.pub_statuses    = PubStatuses()
        self.pub_statuses.load()
        self.review_statuses = ReviewStatuses()
        self.review_statuses.load()
        self.topics          = Topics()
        self.topics.load()
        self.users           = Users()

# Roles

class Roles(LampadasCollection):
    """
    A collection object of all roles.
    """
    
    def load(self):
        sql = "SELECT role_code FROM role"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            role = Role()
            role.load_row(row)
            self.data[role.code] = role
        sql = "SELECT role_code, lang, role_name, role_desc FROM role_i18n"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            role_code = trim(row[0])
            role = self[role_code]
            lang = row[1]
            role.name[lang] = trim(row[2])
            role.description[lang] = trim(row[3])


class Role:
    """
    A role is a way of identifying the role a user plays in the production
    of a document.
    """

    def __init__(self, role_code=None):
        self.name = LampadasCollection()
        self.description = LampadasCollection()
        if role_code==None: return
        self.code = role_code

    def load_row(self, row):
        self.code       = trim(row[0])


# Types

class Types(LampadasCollection):
    """
    A collection object of all document classes (HOWTO, FAQ, etc).
    """
    
    def load(self):
        sql = "SELECT type_code, sort_order FROM type"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            type = Type()
            type.load_row(row)
            self.data[type.code] = type
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT type_code, lang, type_name, type_desc FROM type_i18n"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            type_code = trim(row[0])
            type = self[type_code]
            lang = row[1]
            type.name[lang] = trim(row[2])
            type.description[lang] = trim(row[3])


class Type:
    """
    A type is a way of identifying the type of a document, such as a
    User's Guide, a HOWTO, or a FAQ List.
    """

    def __init__(self, type_code=None):
        self.name = LampadasCollection()
        self.description = LampadasCollection()
        if type_code==None: return
        self.code = type_code

    def load_row(self, row):
        self.code       = trim(row[0])
        self.sort_order = row[1]


# Documents

class Docs(LampadasCollection):
    """
    A collection object providing access to all documents.
    """

    def load(self):
        sql = "SELECT doc_id, title, short_title, type_code, format_code, dtd_code, dtd_version, version, last_update, isbn, pub_status_code, review_status_code, tickle_date, pub_date, tech_review_status_code, maintained, maintainer_wanted, license_code, license_version, copyright_holder, abstract, short_desc, rating, lang, sk_seriesid FROM document"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doc = Doc()
            doc.load_row(row)
            doc.errors.doc_id = doc.id
            doc.files.doc_id = doc.id
            doc.users.doc_id = doc.id
            doc.versions.doc_id = doc.id
            doc.ratings.doc_id = doc.id
            doc.topics.doc_id = doc.id
            doc.notes.doc_id = doc.id
            self[doc.id] = doc
        self.load_errors()
        self.load_users()
        self.load_docfiles()
        self.load_versions()
        self.load_ratings()
        self.load_topics()
        self.load_notes()

    def load_errors(self):
        sql = "SELECT doc_id, err_id, date_entered FROM document_error"
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
        sql = "SELECT doc_id, username, date_entered, vote FROM doc_vote"
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
        sql = "SELECT doc_id, topic_code FROM document_topic"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doc_id = row[0]
            doc = self[doc_id]
            doctopic = DocTopic()
            doctopic.load_row(row)
            doc.topics[doctopic.topic_code] = doctopic

    def load_notes(self):
        sql = 'SELECT note_id, doc_id, date_entered, notes, creator FROM notes'
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doc_id = row[1]
            doc = self[doc_id]
            docnote = DocNote()
            docnote.load_row(row)
            doc.notes[docnote.id] = docnote


# FIXME: try instantiating a new document, then adding *it* to the collection,
# rather than passing in all these parameters. --nico

    def add(self, title, short_title, type_code, format_code, dtd_code, dtd_version, version, last_update, isbn, pub_status_code, review_status_code, tickle_date, pub_date, tech_review_status_code, license_code, license_version, copyright_holder, abstract, short_desc, lang, sk_seriesid):
        id = db.next_id('document', 'doc_id')
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "INSERT INTO document(doc_id, title, short_title, type_code, format_code, dtd_code, dtd_version, version, last_update, isbn, pub_status_code, review_status_code, tickle_date, pub_date, tech_review_status_code, license_code, license_version, copyright_holder, abstract, short_desc, lang, sk_seriesid) VALUES (" + str(id) + ", " + wsq(title) + ", " + wsq(short_title) + ', ' + wsq(type_code) + ", " + wsq(format_code) + ", " + wsq(dtd_code) + ", " + wsq(dtd_version) + ", " + wsq(version) + ", " + wsq(last_update) + ", " + wsq(isbn) + ", " + wsq(pub_status_code) + ", " + wsq(review_status_code) + ", " + wsq(tickle_date) + ", " + wsq(pub_date) + ", " + wsq(tech_review_status_code) + ", " + wsq(license_code) + ", " + wsq(license_version) + ', ' + wsq(copyright_holder) + ', ' + wsq(abstract) + ", " + wsq(short_desc) + ', ' + wsq(lang) + ", " + wsq(sk_seriesid) + ")"
        assert db.runsql(sql)==1
        db.commit()
        doc = Doc(id)
        self[id] = doc
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

        sql = ('DELETE from document WHERE doc_id=' + str(id))
        assert db.runsql(sql)==1
        db.commit()
        del self[id]

class Doc:
    """
    A document in any format, whether local or remote.
    """

    def __init__(self, id=0):
        self.id                      = id
        self.title                   = ''
        self.short_title             = ''
        self.type_code               = ''
        self.format_code             = ''
        self.dtd_code                = ''
        self.dtd_version             = ''
        self.version                 = ''
        self.last_update             = ''
        self.isbn                    = ''
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
        self.topics                  = DocTopics()
        self.topics.doc_id           = self.id
        self.notes                   = DocNotes()
        self.notes.doc_id            = self.id
        if id==0: return
        self.load(id)

    def load(self, id):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT doc_id, title, short_title, type_code, format_code, dtd_code, dtd_version, version, last_update, isbn, pub_status_code, review_status_code, tickle_date, pub_date, tech_review_status_code, maintained, maintainer_wanted, license_code, license_version, copyright_holder, abstract, short_desc, rating, lang, sk_seriesid FROM document WHERE doc_id=" + str(id)
        cursor = db.select(sql)
        row = cursor.fetchone()
        self.load_row(row)
        self.errors                  = DocErrs(self.id)
        self.files                   = DocFiles(self.id)
        self.users                   = DocUsers(self.id)
        self.versions                = DocVersions(self.id)
        self.ratings                 = DocRatings(self.id)
        self.ratings.parent          = self
        self.topics                  = DocTopics(self.id)
        self.notes                   = DocNotes(self.id)

    def load_row(self, row):
        self.id                      = row[0]
        self.title                   = trim(row[1])
        self.short_title             = trim(row[2])
        self.type_code               = trim(row[3])
        self.format_code             = trim(row[4])
        self.dtd_code                = trim(row[5])
        self.dtd_version             = trim(row[6])
        self.version                 = trim(row[7])
        self.last_update             = date2str(row[8])
        self.isbn                    = trim(row[9])
        self.pub_status_code         = trim(row[10])
        self.review_status_code      = trim(row[11])
        self.tickle_date             = date2str(row[12])
        self.pub_date                = date2str(row[13])
        self.tech_review_status_code = trim(row[14])
        self.maintained              = tf2bool(row[15])
        self.maintainer_wanted       = tf2bool(row[16])
        self.license_code            = trim(row[17])
        self.license_version         = trim(row[18])
        self.copyright_holder        = trim(row[19])
        self.abstract                = trim(row[20])
        self.short_desc              = trim(row[21])
        self.rating                  = safeint(row[22])
        self.lang                    = trim(row[23])
        self.sk_seriesid             = trim(row[24])

    def save(self):
        """
        FIXME: use cursor.execute(sql,params) instead! --nico
        """
        # Always recalculate the rating when saving a document.
        self.calc_rating()
        sql = "UPDATE document SET title=" + wsq(self.title) + ', short_title=' + wsq(self.short_title) + ", type_code=" + wsq(self.type_code) + ", format_code=" + wsq(self.format_code) + ", dtd_code=" + wsq(self.dtd_code) + ", dtd_version=" + wsq(self.dtd_version) + ", version=" + wsq(self.version) + ", last_update=" + wsq(self.last_update) + ", isbn=" + wsq(self.isbn) + ", pub_status_code=" + wsq(self.pub_status_code) + ", review_status_code=" + wsq(self.review_status_code) + ", tickle_date=" + wsq(self.tickle_date) + ", pub_date=" + wsq(self.pub_date) + ", tech_review_status_code=" + wsq(self.tech_review_status_code) + ", maintained=" + wsq(bool2tf(self.maintained)) + ', maintainer_wanted=' + wsq(bool2tf(self.maintainer_wanted)) + ", license_code=" + wsq(self.license_code) + ', license_version=' + wsq(self.license_version) + ', copyright_holder=' + wsq(self.copyright_holder) + ", abstract=" + wsq(self.abstract) + ', short_desc=' + wsq(self.short_desc) + ", rating=" + dbint(self.rating) + ", lang=" + wsq(self.lang) + ", sk_seriesid=" + wsq(self.sk_seriesid) + " WHERE doc_id=" + str(self.id)
        db.runsql(sql)
        db.commit()

    def calc_rating(self):
        self.rating = 0
        count = 0
        if self.ratings.count() > 0:
            keys = self.ratings.keys()
            for key in keys:
                self.rating = self.rating + self.ratings[key].rating
                count = count + 1
            self.rating = self.rating / count


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
        sql = "SELECT doc_id, err_id, date_entered FROM document_error WHERE doc_id=" + str(self.doc_id)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doc_err = DocErr()
            doc_err.load_row(row)
            self.data[doc_err.err_id] = doc_err

    def count(self):
        return len(self)
        
    def clear(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "DELETE FROM document_error WHERE doc_id=" + str(self.doc_id)
        db.runsql(sql)
        db.commit()
        self.data = {}

# FIXME: Try instantiating a DocErr object, then adding it to the *document*
# rather than passing all these parameters here. --nico

    def add(self, err_id):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "INSERT INTO document_error(doc_id, err_id) VALUES (" + str(self.doc_id) + ", " + str(err_id) + ')'
        assert db.runsql(sql)==1
        doc_err = DocErr()
        doc_err.doc_id = self.doc_id
        doc_err.err_id = err_id
        doc_err.date_entered = now_string()
        self.data[doc_err.err_id] = doc_err
        db.commit()

class DocErr:
    """
    An error filed against a document by the Lintadas subsystem.
    """

    def load_row(self, row):
        self.doc_id	      = safeint(row[0])
        self.err_id       = safeint(row[1])
        self.date_entered = time2str(row[2])


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
        sql = "SELECT doc_id, username, date_entered, vote FROM doc_vote WHERE doc_id=" + str(self.doc_id)
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
        docrating.date_entered = now_string()
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
        self.doc_id       = row[0]
        self.username     = row[1]
        self.date_entered = time2str(row[2])
        self.rating       = row[3]

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


# DocTopics

class DocTopics(LampadasCollection):
    """
    A collection object providing access to document topics.
    """

    def __init__(self, doc_id=0):
        LampadasCollection.__init__(self)
        self.doc_id = doc_id
        if doc_id > 0:
            self.load()

    def load(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT doc_id, topic_code FROM document_topic WHERE doc_id=" + str(self.doc_id)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            doctopic = DocTopic()
            doctopic.load_row(row)
            self.data[doctopic.topic_code] = doctopic

    def add(self, topic_code):
        sql = 'INSERT INTO document_topic(doc_id, topic_code) VALUES (' + str(self.doc_id) + ', ' + wsq(topic_code) + ')'
        db.runsql(sql)
        db.commit()
        doctopic = DocTopic()
        doctopic.doc_id = self.doc_id
        doctopic.topic_code = topic_code
        self.data[doctopic.topic_code] = doctopic

    def delete(self, topic_code):
        sql = 'DELETE FROM document_topic WHERE doc_id=' + str(self.doc_id) + ' AND topic_code=' + wsq(topic_code)
        db.runsql(sql)
        db.commit()
        del self.data[topic_code]

    def clear(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "DELETE FROM document_topic WHERE doc_id=" + str(self.doc_id)
        db.runsql(sql)
        db.commit()
        self.data = {}

class DocTopic:
    """
    A topic for the document.
    """

    def load_row(self, row):
        self.doc_id   = row[0]
        self.topic_code  = trim(row[1])


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
        sql = 'SELECT note_id, doc_id, date_entered, notes, creator FROM notes WHERE doc_id=' + str(self.doc_id)
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
        docnote.id = note_id
        docnote.doc_id = self.doc_id
        docnote.date_entered = now_string()
        docnote.notes = notes
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
        self.id           = row[0]
        self.doc_id       = row[1]
        self.date_entered = time2str(row[2])
        self.notes        = trim(row[3])
        self.creator      = trim(row[4])


# Licenses

class Licenses(LampadasCollection):
    """
    A collection object of all licenses.
    """
    
    def __init__(self):
        self.data = {}

    def load(self):
        sql = "SELECT license_code, free, sort_order from license"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            license = License()
            license.load_row(row)
            self.data[license.code] = license
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = 'SELECT license_code, lang, license_short_name, license_name, license_desc FROM license_i18n'
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            license_code = trim(row[0])
            license      = self[license_code]
            lang         = row[1]
            license.short_name[lang]  = trim(row[2])
            license.name[lang]        = trim(row[3])
            license.description[lang] = trim(row[4])

class License:
    """
    A documentation or software license.
    """

    def __init__(self, license_code=None, free=None):
        self.short_name = LampadasCollection()
        self.name = LampadasCollection()
        self.description = LampadasCollection()
        if license_code==None: return
        self.code = license_code
        self.free = free

    def load_row(self, row):
        self.code       = trim(row[0])
        self.free       = tf2bool(row[1])
        self.sort_order = row[2]

# DTDs

class DTDs(LampadasCollection):
    """
    A collection object of all DTDs.
    """
    
    def __init__(self):
        self.data = {}

    def load(self):
        sql = "SELECT dtd_code from dtd"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            newDTD = DTD()
            newDTD.load_row(row)
            self.data[newDTD.code] = newDTD

class DTD:
    """
    A Data Type Definition, for SGML and XML documents.
    """

    def __init__(self, dtd_code=''):
        self.code = dtd_code
        if dtd_code=='': return
        self.load()

    def load(self):
        sql = 'SELECT dtd_code FROM dtd WHERE dtd_code=' + wsq(dtd_code)
        cursor = db.select(sql)
        row = cursor.fetchone()
        if row==None: return
        self.load_row(row)

    def load_row(self, row):
        self.code = trim(row[0])


# Errs

class Errors(LampadasCollection):
    """
    A collection object of all errors that can be filed against a document.
    """
    
    def __init__(self):
        self.data = {}
        
    def load(self):
        self.data = {}
        sql = "SELECT err_id FROM error"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            err = Error()
            err.load_row(row)
            self.data[err.id] = err
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT err_id, lang, err_name, err_desc FROM error_i18n"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            err_id                 = row[0]
            err = self[err_id]
            lang                   = row[1]
            err.name[lang]         = trim(row[2])
            err.description[lang]  = trim(row[3])

class Error:
    """
    An error that can be filed against a document.
    """
    
    def __init__(self):
        self.name = LampadasCollection()
        self.description = LampadasCollection()

    def load_row(self, row):
        self.id = row[0]


# Formats

class Formats(LampadasCollection):
    """
    A collection object of all formats.
    """
    
    def __init__(self):
        self.data = {}

    def load(self):
        sql = 'SELECT format_code FROM format'
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            format = Format()
            format.load_row(row)
            self.data[format.code] = format
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT format_code, lang, format_name, format_desc FROM format_i18n"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            format_code = trim(row[0])
            format = self[format_code]
            lang                   = row[1]
            format.name[lang]        = trim(row[2])
            format.description[lang] = trim(row[3])

class Format:
    """
    A file format, for document source files.
    """

    def __init__(self):
        self.name = LampadasCollection()
        self.description = LampadasCollection()

    def load_row(self, row):
        self.code = trim(row[0])


# PubStatuses

class PubStatuses(LampadasCollection):
    """
    A collection object of all publication statuses.
    """
    
    def __init__(self):
        self.data = {}

    def load(self):
        sql = "SELECT pub_status_code, sort_order FROM pub_status"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            newPubStatus = PubStatus()
            newPubStatus.load_row(row)
            self.data[newPubStatus.code] = newPubStatus
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT pub_status_code, lang, pub_status_name, pub_status_desc FROM pub_status_i18n"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            pub_status_code = trim(row[0])
            pub_status = self[pub_status_code]
            lang = row[1]
            pub_status.name[lang] = trim(row[2])
            pub_status.description[lang] = trim(row[3])

class PubStatus:
    """
    The Publication Status defines where in the publication process a
    document is.
    """
    
    def __init__(self, pub_status_code=None):
        self.name = LampadasCollection()
        self.description = LampadasCollection()
        if pub_status_code==None: return
        self.code = pub_status_code

    def load_row(self, row):
        self.code       = trim(row[0])
        self.sort_order = row[1]


# ReviewStatuses

class ReviewStatuses(LampadasCollection):
    """
    A collection object of all publication statuses.
    """
    
    def __init__(self):
        self.data = {}

    def load(self):
        sql = "SELECT review_status_code, sort_order FROM review_status"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            review_status = ReviewStatus()
            review_status.load_row(row)
            self.data[review_status.code] = review_status
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT review_status_code, lang, review_status_name, review_status_desc FROM review_status_i18n"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            review_status_code = trim(row[0])
            review_status = self[review_status_code]
            lang = row[1]
            review_status.name[lang] = trim(row[2])
            review_status.description[lang] = trim(row[3])

class ReviewStatus:
    """
    The Review Status defines where in the review process a
    document is.
    """
    
    def __init__(self, review_status_code=None):
        self.name = LampadasCollection()
        self.description = LampadasCollection()
        if review_status_code==None: return
        self.code = review_status_code

    def load_row(self, row):
        self.code       = trim(row[0])
        self.sort_order = row[1]


# Topics

class Topics(LampadasCollection):
    """
    A collection object of all topics.
    """
    
    def __init__(self):
        self.data = {}

    def load(self):
        sql = "SELECT parent_code, topic_code, sort_order FROM topic"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            topic = Topic()
            topic.load_row(row)
            self.data[topic.code] = topic
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT topic_code, lang, topic_name, topic_desc FROM topic_i18n"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            topic_code = trim(row[0])
            topic = self[topic_code]
            lang = row[1]
            topic.name[lang] = trim(row[2])
            topic.description[lang] = trim(row[3])
        self.calc_titles()

    def calc_titles(self):
        for topic_code in self.sort_by('sort_order'):
            topic = self[topic_code]
            topic.title = LampadasCollection()
            parent_code = topic.parent_code
            for lang in languages.supported_keys():
                topic.title[lang] = ''
                if parent_code > '':
                    topic.title[lang] = self[parent_code].title[lang] + ': '
                topic.title[lang] = topic.title[lang] + topic.name[lang]
    
class Topic:
    """
    Each document can be assigned an arbitrary number of topics.
    The web interface allows a user to browse through document topics,
    to help them find a document on the subject in which they are interested.
    """

    def __init__(self, parent_code='', topic_code='', sort_order=0):
        self.name = LampadasCollection()
        self.description = LampadasCollection()
        self.parent_code = parent_code
        self.code        = topic_code
        self.sort_order  = sort_order
        self.docs = TopicDocs(topic_code)

    def load_row(self, row):
        self.parent_code = trim(row[0])
        self.code        = trim(row[1])
        self.sort_order  = safeint(row[2])
        self.docs        = TopicDocs(self.code)


# SubtopicDocs

class TopicDocs(LampadasCollection):

    def __init__(self, topic_code):
        self.data = {}
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = 'SELECT doc_id FROM document_topic WHERE topic_code=' + wsq(topic_code)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            topicdoc = TopicDoc()
            topicdoc.topic_code = topic_code
            topicdoc.doc_id = row[0]
            self.data[topicdoc.doc_id] = topicdoc

class TopicDoc:

    def __init__(self):
        pass
    
        
# UserDocs

class UserDocs(LampadasCollection):
    """
    A collection object providing access to all user document associations.
    """

    def __init__(self, username):
        self.data = {}
        self.username = username
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT doc_id, username, role_code, email, active FROM document_user WHERE username=" + wsq(username)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            newUserDoc = UserDoc()
            newUserDoc.load_row(row)
            self.data[newUserDoc.doc_id] = newUserDoc


    def add(self, doc_id, role_code, email, active):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "INSERT INTO document_user(doc_id, username, role_code, email, active) VALUES (" + str(doc_id) + ", " + wsq(self.username) + ", " + wsq(role_code) + ", " + wsq(email) + ", " + wsq(bool2tf(active)) +  " )"
        assert db.runsql(sql)==1
        db.commit()
        newUserDoc = UserDoc()
        self.data[doc_id] = newUserDoc
    
    def delete(self, doc_id):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = 'DELETE from document_user WHERE doc_id=' + str(doc_id) + ' AND username=' + wsq(self.username)
        assert db.runsql(sql)==1
        db.commit()
        del self.data[doc_id]

class UserDoc:
    """
    An association between a user and a document. This association defines the role
    which the user plays in the production of the document.
    """

    def load_row(self, row):
        self.doc_id		= row[0]
        self.username	= trim(row[1])
        self.role		= trim(row[2])
        self.email		= trim(row[3])
        self.active		= tf2bool(row[4])

    def save(self):
        """
        FIXME: use cursor.execute(sql,params) instead! --nico
        """
        sql = "UPDATE document_user SET role=" + wsq(self.role) + ", email=" + wsq(self.email) + ", active=" + wsq(bool2tf(self.active)) + " WHERE doc_id=" + str(self.doc_id) + " AND username=" + wsq(self.username)
        db.runsql(sql)
        db.commit()


# Users

class Users:
    """
    A collection object providing access to registered users.
    """

    def __getitem__(self, username):
        user = User(username)
        if user.username==username:
            return User(username)
        else:
            return None

    def count(self):
        return db.read_value('SELECT count(*) from username')

    def add(self, username, first_name, middle_name, surname, email, admin, sysadmin, password, notes, stylesheet):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "INSERT INTO username (username, first_name, middle_name, surname, email, admin, sysadmin, password, notes, stylesheet) VALUES (" + wsq(username) + ", " + wsq(first_name) + ", " + wsq(middle_name) + ", " + wsq(surname) + ", " + wsq(email) + ", " + wsq(bool2tf(admin)) + ", " + wsq(bool2tf(sysadmin)) + ", " + wsq(password) + ", " + wsq(notes) + ", " + wsq(stylesheet) + ")"
        assert db.runsql(sql)==1
        db.commit()
        user = self[username]
        return user
    
    def delete(self, username):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = 'DELETE from username WHERE username=' + wsq(username)
        assert db.runsql(sql)==1
        db.commit()

    def is_email_taken(self, email):
        value = db.read_value('SELECT COUNT(*) FROM username WHERE email=' + wsq(email))
        return value

    def find_session_user(self, session_id):
        """
        Looks a session_id up in the username table, to see which user owns the session.
        """

        log(3, 'looking for user session: ' + session_id)
        if session_id > '':
        # FIXME: use cursor.execute(sql,params) instead! --nico
            sql = 'SELECT username FROM username WHERE session_id=' + wsq(session_id)
            cursor = db.select(sql)
            row = cursor.fetchone()
            if row:
                log(3, 'found user session: ' + row[0])
                return trim(row[0])
        return ''

    def find_email_user(self, email):
        sql = 'SELECT username FROM username WHERE email=' + wsq(email)
        cursor = db.select(sql)
        row = cursor.fetchone()
        if row:
            username = trim(row[0])
            user = self[username]
            return user
        
    def letter_keys(self, letter):
        keys = []
        sql = 'SELECT username FROM username WHERE upper(substr(username,1,1))=' + wsq(letter.upper())
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            username = trim(row[0])
            keys = keys + [username]
        keys.sort()
        return keys
        
class User:
    """
    A user who is known by the system can login to manipulate documents
    and act on the database according to his rights.
    """

    def __init__(self, username='') :
        self.username       = ''
        self.session_id     = ''
        self.first_name     = ''
        self.middle_name    = ''
        self.surname        = ''
        self.email          = ''
        self.admin          = 0
        self.sysadmin       = 0
        self.password       = ''
        self.notes          = ''
        self.stylesheet     = ''
        self.name           = ''

        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = 'SELECT username, session_id, first_name, middle_name, surname, email, admin, sysadmin, password, notes, stylesheet FROM username WHERE username=' + wsq(username)
        cursor = db.select(sql)
        row = cursor.fetchone()
        if row==None:
            return
        self.username       = trim(row[0])
        self.session_id     = trim(row[1])
        self.first_name     = trim(row[2])
        self.middle_name    = trim(row[3])
        self.surname        = trim(row[4])
        self.email          = trim(row[5])
        self.admin          = tf2bool(row[6])
        self.sysadmin       = tf2bool(row[7])
        self.password       = trim(row[8])
        self.notes          = trim(row[9])
        self.stylesheet     = trim(row[10])
        self.name           = trim(trim(self.first_name + ' ' + self.middle_name) + ' ' + self.surname)

        self.docs = UserDocs(self.username)

    def save(self):
        """
        FIXME: use cursor.execute(sql,params) instead! --nico
        """
        sql = 'UPDATE username SET session_id=' + wsq(self.session_id) + ', first_name=' + wsq(self.first_name) + ', middle_name=' + wsq(self.middle_name) + ', surname=' + wsq(self.surname) + ', email=' + wsq(self.email) + ', admin=' + wsq(bool2tf(self.admin)) + ', sysadmin=' + wsq(bool2tf(self.sysadmin)) + ', password=' + wsq(self.password) + ', notes=' + wsq(self.notes) + ', stylesheet=' + wsq(self.stylesheet) + ' WHERE username=' + wsq(self.username)
        db.runsql(sql)
        db.commit()

    def can_edit(self, doc_id=None, username=None):
        if self.admin > 0 or self.sysadmin > 0:
            return 1
        if not doc_id==None:
            if self.docs.has_key(doc_id):
                return 1
            if doc_id==0:
                return 1
        if not username==None:
            if username==self.username:
                return 1
        return 0
        


lampadas = Lampadas()


# main
if __name__=='__main__' :
    pass
