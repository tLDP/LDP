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
# the imported module changes or makes a mistake

from Globals import *
from BaseClasses import *
from Config import config
from Database import db
from Log import log


#log(2, '               **********Initializing DataLayer**********')
#db.connect(config.db_type, config.db_name)

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
        self.classes        = Classes()
        self.classes.Load()
        self.Config         = Cfg()
        self.Docs           = Docs()
        self.Docs.Load()
        self.Licenses       = Licenses()
        self.DTDs           = DTDs()
        self.Formats        = Formats()
        self.languages      = Languages()
        self.PubStatuses    = PubStatuses()
        self.ReviewStatuses = ReviewStatuses()
        self.topics         = Topics()
        self.subtopics      = Subtopics()
        self.users          = Users()

    def user(self, username):
        return User(username)

    def Doc(self, DocID):
        return Doc(DocID)


# Class

class Classes(LampadasCollection):
    """
    A collection object of all document classes (HOWTO, FAQ, etc).
    """
    
    def Load(self):
        sql = "SELECT class_code, sort_order FROM class"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newClass = Class()
            newClass.Load(row)
            self.data[newClass.code] = newClass

class Class:
    """
    A class is a way of identifying the type of a document, such as a
    User's Guide, a HOWTO, or a FAQ List.
    """

    def __init__(self, class_code=None):
        self.name = LampadasCollection()
        self.description = LampadasCollection()
        if class_code==None: return
        self.code = class_code

    def Load(self, row):
        self.code       = trim(row[0])
        self.sort_order = row[1]

        sql = "SELECT lang, class_name, class_desc FROM class_i18n WHERE class_code=" + wsq(self.code)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            lang = row[0]
            self.name[lang] = trim(row[1])
            self.description[lang] = trim(row[2])


# Cfg

class Cfg(LampadasCollection):
    """
    Holds system configuration information.
    """

    def __init__(self):
        self.data = {}
        self.Load()

    def __call__(self, key):
        return self[key]

    def Load(self):
        sql = "SELECT name, value FROM config"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            self.data[trim(row[0])] = trim(row[1])


# Documents

class Docs(LampadasCollection):
    """
    A collection object providing access to all documents.
    """

    def Load(self):
        sql = "SELECT doc_id, title, class_code, format_id, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating, lang, sk_seriesid FROM document"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newDoc = Doc()
            newDoc.LoadRow(row)
            self[newDoc.ID] = newDoc

# FIXME: try instantiating a new document, then adding *it* to the collection,
# rather than passing in all these parameters.

    def add(self, Title, class_code, FormatID, DTD, DTDVersion, Version, LastUpdate, URL, ISBN, PubStatusCode, ReviewStatus, TickleDate, PubDate, HomeURL, TechReviewStatusCode, License, Abstract, Lang, SeriesID):
        self.id = db.read_value('SELECT max(doc_id) from document') + 1
        sql = "INSERT INTO document(doc_id, title, class_code, format_id, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, license, abstract, lang, sk_seriesid) VALUES (" + str(self.id) + ", " + wsq(Title) + ", " + wsq(class_code) + ", " + dbint(FormatID) + ", " + wsq(DTD) + ", " + wsq(DTDVersion) + ", " + wsq(Version) + ", " + wsq(LastUpdate) + ", " + wsq(URL) + ", " + wsq(ISBN) + ", " + wsq(PubStatusCode) + ", " + wsq(ReviewStatus) + ", " + wsq(TickleDate) + ", " + wsq(PubDate) + ", " + wsq(HomeURL) + ", " + wsq(TechReviewStatusCode) + ", " + wsq(License) + ", " + wsq(Abstract) + ", " + wsq(Lang) + ", " + wsq(SeriesID) + ")"
        assert db.runsql(sql) == 1
        db.commit()
        self.NewID = db.read_value('SELECT MAX(doc_id) from document')
        newDoc = Doc(self.NewID)
        self[self.NewID] = newDoc
        return self.NewID
    
    def Del(self, id):
        sql = ('DELETE from document WHERE doc_id=' + str(id))
        assert db.runsql(sql) == 1
        db.commit()
        del self[id]

class Doc:
    """
    A document in any format, whether local or remote.
    """

    def __init__(self, id=None):
        if id == None: return
        self.Load(id)

    def Load(self, id):
        sql = "SELECT doc_id, title, class_code, format_id, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating, lang, sk_seriesid FROM document WHERE doc_id=" + str(id)
        cursor = db.select(sql)
        row = cursor.fetchone()
        self.LoadRow(row)

    def LoadRow(self, row):
        self.ID                     = row[0]
        self.Title                  = trim(row[1])
        self.class_code             = trim(row[2])
        self.FormatID               = row[3]
        self.DTD                    = trim(row[4])
        self.DTDVersion             = trim(row[5])
        self.Version                = trim(row[6])
        self.LastUpdate             = date2str(row[7])
        self.URL                    = trim(row[8])
        self.ISBN                   = trim(row[9])
        self.PubStatusCode          = trim(row[10])
        self.ReviewStatusCode       = trim(row[11])
        self.TickleDate             = date2str(row[12])
        self.PubDate                = date2str(row[13])
        self.HomeURL                = trim(row[14])
        self.TechReviewStatusCode	= trim(row[15])
        self.Maintained             = tf2bool(row[16])
        self.License                = trim(row[17])
        self.Abstract               = trim(row[18])
        self.Rating                 = safeint(row[19])
        self.Lang                   = trim(row[20])
        self.SeriesID               = trim(row[21])
        self.Errs                   = DocErrs(self.ID)
        self.Files                  = DocFiles(self.ID)
        self.Ratings                = DocRatings(self.ID)
        self.Ratings.Parent         = self
        self.Versions               = DocVersions(self.ID)

    def Save(self):
        sql = "UPDATE document SET title=" + wsq(self.Title) + ", class_code=" + wsq(self.class_code) + ", format_id=" + dbint(self.FormatID) + ", dtd=" + wsq(self.DTD) + ", dtd_version=" + wsq(self.DTDVersion) + ", version=" + wsq(self.Version) + ", last_update=" + wsq(self.LastUpdate) + ", url=" + wsq(self.URL) + ", isbn=" + wsq(self.ISBN) + ", pub_status=" + wsq(self.PubStatusCode) + ", review_status=" + wsq(self.ReviewStatusCode) + ", tickle_date=" + wsq(self.TickleDate) + ", pub_date=" + wsq(self.PubDate) + ", ref_url=" + wsq(self.HomeURL) + ", tech_review_status=" + wsq(self.TechReviewStatusCode) + ", maintained=" + wsq(bool2tf(self.Maintained)) + ", license=" + wsq(self.License) + ", abstract=" + wsq(self.Abstract) + ", rating=" + dbint(self.Rating) + ", lang=" + wsq(self.Lang) + ", sk_seriesid=" + wsq(self.SeriesID) + " WHERE doc_id=" + str(self.ID)
        db.runsql(sql)
        db.commit()


# DocErrs

class DocErrs(LampadasList):
    """
    A collection object providing access to all document errors, as identified by the
    Lintadas subsystem.
    """

    def __init__(self, DocID):
        LampadasList.__init__(self)
        assert not DocID == None
        self.DocID = DocID
        sql = "SELECT err_id FROM document_error WHERE doc_id=" + str(DocID)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newDocErr = DocErr()
            newDocErr.Load(DocID, row)
            self.list = self.list + [newDocErr]

    def Clear(self):
        sql = "DELETE FROM document_error WHERE doc_id=" + str(self.DocID)
        db.runsql(sql)
        db.commit()
        self.list = []

# FIXME: Try instantiating a DocErr object, then adding it to the *document*
# rather than passing all these parameters here.

    def add(self, ErrID):
        sql = "INSERT INTO document_error(doc_id, err_id) VALUES (" + str(self.DocID) + ", " + wsq(ErrID)
        assert db.runsql(sql) == 1
        newDocErr = DocErr()
        newDocErr.DocID = self.DocID
        newDocErr.ErrID = ErrID
        self.list = self.list + [newDocErr]
        db.commit()

class DocErr:
    """
    An error filed against a document by the Lintadas subsystem.
    """

    def Load(self, DocID, row):
        assert not DocID == None
        assert not row == None
        self.DocID	= DocID
        self.ErrID	= safeint(row[0])


# DocFiles

class DocFiles(LampadasCollection):
    """
    A collection object providing access to all document source files.
    """

    def __init__(self, DocID):
        self.data = {}
        assert not DocID == None
        self.DocID = DocID
        sql = "SELECT filename, format_id FROM document_file WHERE doc_id=" + str(DocID)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newDocFile = DocFile()
            newDocFile.Load(DocID, row)
            self.data[newDocFile.Filename] = newDocFile

    def add(self, DocID, Filename, FormatID=None):
        sql = 'INSERT INTO document_file (doc_id, filename, format_id) VALUES (' + str(DocID) + ', ' + wsq(Filename) + ', ' + dbint(FormatID) + ')'
        assert db.runsql(sql) == 1
        db.commit()
        newDocFile = DocFile()
        newDocFile.DocID = DocID
        newDocFile.Filename = Filename
        newDocFile.FormatID = FormatID
        
    def Clear(self):
        sql = "DELETE FROM document_file WHERE doc_id=" + str(self.DocID)
        db.runsql(sql)
        db.commit()
        self.data = {}

class DocFile:
    """
    An association between a document and a file.
    """

    import os.path

    def Load(self, DocID, row):
        assert not DocID == None
        assert not row == None
        self.DocID	= DocID
        self.Filename	= trim(row[0])
        self.FormatID	= row[1]
        if self.Filename[:5] == 'http:' or self.Filename[:4] == 'ftp:':
            self.IsLocal = 0
        else:
            self.IsLocal = 1
        self.file_only	= self.os.path.split(self.Filename)[1]
        self.basename	= self.os.path.splitext(self.file_only)[0]
        
        # FIXME: this is a stub. We need a new field in the database.
        
        self.is_primary	= self.IsLocal
        
    def Save(self):
        sql = "UPDATE document_file SET format_id=" + dbint(self.FormatID) + " WHERE doc_id=" + str(self.DocID) + " AND filename=" + wsq(self.Filename)
        db.runsql(sql)
        db.commit()

    def Del(self):
        sql = "DELETE FROM document_file WHERE doc_id=" + str(self.DocID) + " AND filename=" + wsq(self.Filename)
        db.runsql(sql)
        db.commit()


# DocRatings

class DocRatings(LampadasCollection):
    """
    A collection object providing access to all ratings placed on documents by users.
    """

    def __init__(self, DocID):
        self.data = {}
        self.Parent = None
        assert not DocID == None
        self.DocID = DocID
        sql = "SELECT user_id, date_entered, vote FROM doc_vote WHERE doc_id=" + str(DocID)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newDocRating = DocRating()
            newDocRating.Load(DocID, row)
            self.data[newDocRating.UserID] = newDocRating
        self.CalcAverage()

    def add(self, UserID, Rating):
        newDocRating = DocRating()
        newDocRating.DocID	= self.DocID
        newDocRating.UserID	= UserID
        newDocRating.Rating	= Rating
        newDocRating.Save()
        self.data[newDocRating.UserID] = newDocRating
        self.CalcAverage()

    def Del(self, UserID):
        if self.data[UserID] == None: return
        del self.data[UserID]
        sql = 'DELETE FROM doc_vote WHERE doc_id=' + str(self.DocID) + ' AND user_id=' + str(UserID)
        db.runsql(sql)
        self.CalcAverage()
        
    def Clear(self):
        sql = "DELETE FROM doc_vote WHERE doc_id=" + str(self.DocID)
        db.runsql(sql)
        self.data = {}
        self.CalcAverage()

    def CalcAverage(self):
        self.Average = 0
        if self.count() > 0:
            keys = self.data.keys()
            for key in keys:
                self.Average = self.Average + self.data[key].Rating
            self.Average = self.Average / self.count()
        sql = "UPDATE document SET rating=" + str(self.Average) + " WHERE doc_id=" + str(self.DocID)
#		db.runsql(sql)
#		db.commit()
        if not self.Parent == None:
            self.Parent.Rating = self.Average

class DocRating:
    """
    A rating of a document, assigned by a registered user.
    """

    def Load(self, DocID, row):
        assert not DocID == None
        assert not row == None
        self.DocID		= DocID
        self.UserID		= row[0]
        self.DateEntered	= trim(row[1])
        self.Rating		= row[2]

    def Save(self):
        sql = "DELETE from doc_vote WHERE doc_id=" + str(self.DocID) + " AND user_id=" + str(self.UserID)
        db.runsql(sql)
        sql = "INSERT INTO doc_vote (doc_id, user_id, vote) VALUES (" + str(self.DocID) + ", " + str(self.UserID) + ", " + str(self.Rating) + ")"
        db.runsql(sql)
        db.commit()


# DocVersions

class DocVersions(LampadasCollection):
    """
    A collection object providing access to document revisions.
    """

    def __init__(self, DocID):
        LampadasCollection.__init__(self)
        assert not DocID == None
        self.DocID = DocID
        sql = "SELECT rev_id, version, pub_date, initials, notes FROM document_rev WHERE doc_id=" + str(DocID)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newDocVersion = DocVersion()
            newDocVersion.Load(DocID, row)
            self.data[newDocVersion.ID] = newDocVersion

class DocVersion:
    """
    A release of the document.
    """

    def Load(self, DocID, row):
        assert not DocID == None
        assert not row == None
        self.DocID	= DocID
        self.ID		= row[0]
        self.Version	= trim(row[1])
        self.PubDate	= date2str(row[2])
        self.Initials	= trim(row[3])
        self.Notes	= trim(row[4])

    def Save(self):
        sql = "UPDATE document_rev SET version=" + wsq(self.Version) + ", pub_date=" + wsq(self.PubDate) + ", initials=" + wsq(self.Initials) + ", notes=" + wsq(self.Notes) + "WHERE doc_id=" + str(self.DocID) + " AND rev_id" + wsq(self.ID)
        assert db.runsql(sql) == 1
        db.commit()


# Licenses

class Licenses(LampadasCollection):
    """
    A collection object of all Licenses.
    """
    
    def __init__(self):
        self.data = {}
        sql = "SELECT license, free from license"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newLicense = License()
            newLicense.Load(row)
            self.data[newLicense.License] = newLicense

class License:
    """
    A documentation or software license.
    """

    def __init__(self, License=None, Free=None):
        if License==None: return
        self.License = License
        self.Free = Free

    def Load(self, row):
        self.License    = trim(row[0])
        self.Free       = tf2bool(row[1])


# DTDs

class DTDs(LampadasCollection):
    """
    A collection object of all DTDs.
    """
    
    def __init__(self):
        self.data = {}
        sql = "SELECT dtd from dtd"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newDTD = DTD()
            newDTD.Load(row)
            self.data[newDTD.DTD] = newDTD

class DTD:
    """
    A Data Type Definition, for SGML and XML documents.
    """

    def __init__(self, DTD=None):
        if DTD==None: return
        self.DTD = DTD

    def Load(self, row):
        self.DTD = trim(row[0])


# Errs

class Errs(LampadasCollection):
    """
    A collection object of all errors that can be filed against a document.
    """
    
    def __init__(self):
        self.data = {}
        sql = "SELECT err_id FROM error"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newErr = Err()
            newErr.Load(row)
            self.data[newErr.ErrID] = newErr

class Err:
    """
    An error that can be filed against a document.
    """
    
    def __init__(self, ErrID=None):
        self.name = LampadasCollection()
        self.description = LampadasCollection()
        if Err==None: return
        self.ErrID = ErrID

    def Load(self, row):
        self.ErrID = trim(row[0])
        sql = "SELECT lang, err_name, err_desc FROM error_i18n WHERE err_id=" + wsq(self.ErrID)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            lang		= row[0]
            self.name[lang]        = trim(row[1])
            self.description[lang] = trim(row[1])


# Formats

class Formats(LampadasCollection):
    """
    A collection object of all formats.
    """
    
    def __init__(self):
        self.data = {}
        sql = "SELECT format_id FROM format"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newFormat = Format()
            newFormat.Load(row)
            self.data[newFormat.ID] = newFormat

class Format:
    """
    A file format, for document source files.
    """

    def __init__(self, FormatID=None):
        self.name = LampadasCollection()
        self.description = LampadasCollection()
        if FormatID==None: return
        self.ID = FormatID

    def Load(self, row):
        self.ID = row[0]
        sql = "SELECT lang, format_name, format_desc FROM format_i18n WHERE format_id=" + str(self.ID)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            lang		= row[0]
            self.name[lang]        = trim(row[1])
            self.description[lang] = trim(row[2])


# Languages

class Languages(LampadasCollection):
    """
    A collection object of all languages supported by the ISO 639
    standard.
    """

    def __init__(self):
        self.data = {}
        sql = "SELECT lang_code, supported FROM language"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newLanguage = Language()
            newLanguage.load(row)
            self.data[newLanguage.code] = newLanguage

class Language:
    """
    Defines a language supported by Lampadas. Documents can be translated into,
    and Lampadas can be localized for, any language supported by ISO 639.
    """

    def __init__(self, lang_code=None):
        if lang_code==None: return
        self.code = lang_code
        sql = "SELECT lang_code, supported FROM language WHERE lang_code= " + wsq(lang_code)
        cursor = db.select(sql)
        self.load(sql)

    def load(self, row):
        self.code      = trim(row[0])
        self.supported = tf2bool(row[1])
        self.name = LampadasCollection()
        sql = "SELECT lang, lang_name FROM language_i18n WHERE lang_code=" + wsq(self.code)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            lang = row[0]
            self.name[lang] = trim(row[1])


# PubStatuses

class PubStatuses(LampadasCollection):
    """
    A collection object of all publication statuses.
    """
    
    def __init__(self):
        self.data = {}
        sql = "SELECT pub_status FROM pub_status"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newPubStatus = PubStatus()
            newPubStatus.Load(row)
            self.data[newPubStatus.Code] = newPubStatus

class PubStatus:
    """
    The Publication Status defines where in the publication process a
    document is.
    """
    
    def __init__(self, PubStatusCode=None):
        self.name = LampadasCollection()
        self.description = LampadasCollection()
        if PubStatusCode==None: return
        self.Code = PubStatusCode

    def Load(self, row):
        self.Code = trim(row[0])
        sql = "SELECT lang, pub_status_name, pub_status_desc FROM pub_status_i18n WHERE pub_status=" + wsq(self.Code)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            lang = row[0]
            self.name[lang] = trim(row[1])
            self.description[lang] = trim(row[2])


# ReviewStatuses

class ReviewStatuses(LampadasCollection):
    """
    A collection object of all publication statuses.
    """
    
    def __init__(self):
        self.data = {}
        sql = "SELECT review_status FROM review_status"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newReviewStatus = ReviewStatus()
            newReviewStatus.Load(row)
            self.data[newReviewStatus.Code] = newReviewStatus

class ReviewStatus:
    """
    The Reviewlication Status defines where in the publication process a
    document is.
    """
    
    def __init__(self, ReviewStatusCode=None):
        self.name = LampadasCollection()
        self.description = LampadasCollection()
        if ReviewStatusCode==None: return
        self.Code = ReviewStatusCode

    def Load(self, row):
        self.Code = trim(row[0])
        sql = "SELECT lang, review_status_name, review_status_desc FROM review_status_i18n WHERE review_status=" + wsq(self.Code)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            lang = row[0]
            self.name[lang] = trim(row[1])
            self.description[lang] = trim(row[2])


# Topics

class Topics(LampadasCollection):
    """
    A collection object of all topics.
    """
    
    def __init__(self):
        self.data = {}
        sql = "SELECT topic_code, topic_num FROM topic"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newTopic = Topic()
            newTopic.Load(row)
            self.data[newTopic.code] = newTopic

class Topic:
    """
    Each document can be assigned an arbitrary number of topics.
    The web interface allows a user to browse through document topics,
    to help them find a document on the subject in which they are interested.
    """

    def __init__(self, TopicCode=None, TopicNum=None):
        self.name = LampadasCollection()
        self.description = LampadasCollection()
        if TopicCode==None: return
        self.code = TopicCode
        self.num  = TopicNum

    def Load(self, row):
        self.code = trim(row[0])
        self.num  = safeint(row[1])
        sql = "SELECT lang, topic_name, topic_desc FROM topic_i18n WHERE topic_code=" + wsq(self.code)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            lang = row[0]
            self.name[lang] = trim(row[1])
            self.description[lang] = trim(row[2])


# Subtopics

class Subtopics(LampadasCollection):
    """
    A collection object of all subtopics.
    """
    
    def __init__(self):
        self.data = {}
        sql = "SELECT subtopic_code, subtopic_num, topic_code FROM subtopic"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newSubtopic = Subtopic()
            newSubtopic.load(row)
            self.data[newSubtopic.code] = newSubtopic

class Subtopic:
    """
    Each document can be assigned an arbitrary number of topics.
    The web interface allows a user to browse through document topics,
    to help them find a document on the subject in which they are interested.
    """

    def __init__(self, subtopic_code=None, subtopic_num=None, topic_code=None):
        self.name = LampadasCollection()
        self.description = LampadasCollection()
        if subtopic_code==None: return
        self.code       = subtopic_code
        self.num        = subtopic_num
        self.topic_code = subtopic_code
        self.docs       = SubtopicDocs(subtopic_code)

    def load(self, row):
        self.code       = trim(row[0])
        self.num        = safeint(row[1])
        self.topic_code = trim(row[2])
        self.docs       = SubtopicDocs(self.code)
        sql = "SELECT lang, subtopic_name, subtopic_desc FROM subtopic_i18n WHERE subtopic_code=" + wsq(self.code)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            lang = row[0]
            self.name[lang] = trim(row[1])
            self.description[lang] = trim(row[2])


# SubtopicDocs

class SubtopicDocs(LampadasCollection):

    def __init__(self, subtopic_code):
        self.data = {}
        sql = 'SELECT doc_id FROM document_topic WHERE subtopic_code=' + wsq(subtopic_code)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newSubtopicDoc = SubtopicDoc()
            newSubtopicDoc.subtopic_code = subtopic_code
            newSubtopicDoc.doc_id = row[0]
            self.data[newSubtopicDoc.doc_id] = newSubtopicDoc

class SubtopicDoc:

    def __init__(self):
        pass
    
        
# Users

class Users:
    """
    A collection object providing access to registered users.
    """

    def __getitem__(self, username):
        return User(username)

    def count(self):
        return db.read_value('SELECT count(*) from username')

    def add(self, username, first_name, middle_name, surname, email, admin, sysadmin, password, notes, stylesheet):
        sql = "INSERT INTO username (username, first_name, middle_name, surname, email, admin, sysadmin, password, notes, stylesheet) VALUES (" + wsq(username) + ", " + wsq(first_name) + ", " + wsq(middle_name) + ", " + wsq(surname) + ", " + wsq(email) + ", " + wsq(bool2tf(admin)) + ", " + wsq(bool2tf(sysadmin)) + ", " + wsq(password) + ", " + wsq(notes) + ", " + wsq(stylesheet) + ")"
        assert db.runsql(sql) == 1
        db.commit()
    
    def delete(self, username):
        sql = 'DELETE from username WHERE username=' + wsq(username)
        assert db.runsql(sql) == 1
        db.commit()

    def is_email_taken(self, email):
        value = db.read_value('SELECT COUNT(*) FROM username WHERE email=' + wsq(email))
        return value

    def find_session_user(self, session_id):
        log(3, 'looking for user session: ' + session_id)
        if session_id > '':
            sql = 'SELECT username FROM username WHERE session_id=' + wsq(session_id)
            cursor = db.select(sql)
            row = cursor.fetchone()
            if row:
                log(3, 'found user session: ' + row[0])
                return trim(row[0])
        return ''


class User:
    """
    A user who is known by the system can login to manipulate documents
    and act on the database according to his rights.
    """

    def __init__(self, username) :
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

        sql = 'SELECT username, session_id, first_name, middle_name, surname, email, admin, sysadmin, password, notes, stylesheet FROM username WHERE username=' + wsq(username)
        cursor = db.select(sql)
        row = cursor.fetchone()
        if row == None:
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
        sql = 'UPDATE username SET session_id=' + wsq(self.session_id) + ', first_name=' + wsq(self.first_name) + ', middle_name=' + wsq(self.middle_name) + ', surname=' + wsq(self.surname) + ', email=' + wsq(self.email) + ', admin=' + wsq(bool2tf(self.admin)) + ', sysadmin=' + wsq(bool2tf(self.sysadmin)) + ', password=' + wsq(self.password) + ', notes=' + wsq(self.notes) + ', stylesheet=' + wsq(self.stylesheet) + ' WHERE username=' + wsq(self.username)
        db.runsql(sql)
        db.commit()


# UserDocs

class UserDocs(LampadasList):
    """
    A collection object providing access to all user document associations.
    """

    def __init__(self, username):
        #print "Loading user docs for user: " + str(UserID)
        LampadasList.__init__(self)
        assert not username == None
        self.username = username
        sql = "SELECT doc_id, username, role, email, active FROM document_user WHERE username=" + wsq(username)
        cursor = db.select(sql)
        #print sql
        while (1):
            #print "Loading UserDocs row"
            row = cursor.fetchone()
            if row == None: break
            #print "Loaded UserDocs row"
            newUserDoc = UserDoc(row[0], username)
            self.list = self.list + [newUserDoc]

    def add(self, DocID, Role, Email, Active):
        sql = "INSERT INTO document_user(doc_id, username, role, email, active) VALUES (" + str(DocID) + ", " + wsq(self.username) + ", " + wsq(Role) + ", " + wsq(Email) + ", " + wsq(bool2tf(Active)) +  " )"
        assert db.runsql(sql) == 1
        db.commit()
    
    def Del(self, DocID):
        sql = 'DELETE from document_user WHERE doc_id=' + str(DocID) + ' AND username=' + wsq(self.username)
        assert db.runsql(sql) == 1
        db.commit()
        del self.col[DocID]

class UserDoc(Doc):
    """
    An association between a user and a document. This association defines the role
    which the user plays in the production of the document.
    """

    def __init__(self, DocID=None, username=None):
        #print "initializing UserDoc, DocID: " + str(DocID) + ", UserID: " + str(UserID)
        Doc.__init__(self, DocID)
        self.DocID = DocID
        self.username = username
        #print "UserDoc.UserID: " + str(UserID)
        if DocID == None: return
        if username == None: return
        #print "Calling UserDoc.load"
        self.Load(DocID, username)

    def Load(self, DocID=None, username=None):
        #print "Loading UserDoc, DocID: " + str(DocID) + ", UserID: " + str(UserID)
        if not DocID == None:
            self.DocID = DocID
        assert not self.DocID == None
        if not username == None:
            self.username = username
        assert not self.username == None
        sql = "SELECT doc_id, username, role, email, active FROM document_user WHERE doc_id=" + str(self.DocID) + " AND user_id=" + wsq(self.username)
        cursor = db.select(sql)
        row = cursor.fetchone()
        self.LoadRow(row)
        Doc.Load(self, self.DocID)

    def LoadRow(self, row):
        assert not row == None
        self.DocID		= row[0]
        self.username	= trim(row[1])
        self.Role		= trim(row[2])
        self.Email		= trim(row[3])
        self.Active		= tf2bool(row[4])

    def Save(self):
        sql = "UPDATE document_user SET role=" + wsq(self.Role) + ", email=" + wsq(self.Email) + ", active=" + wsq(bool2tf(self.Active)) + " WHERE doc_id=" + str(self.DocID) + " AND username=" + wsq(self.username)
        db.runsql(sql)
        db.commit()
        Doc.Save(self)
    

lampadas = Lampadas()


# main
if __name__ == '__main__' :
    print "Running unit tests..."
    string = "foo"
    assert wsq(string) == "'foo'"
    string = "it's"
    assert wsq(string) == "'it''s'"
    string = "it's that's"
    assert wsq(string) == "'it''s that''s'"
    print "End unit test run."
    
