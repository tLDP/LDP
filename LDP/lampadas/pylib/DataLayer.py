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


# Globals

db.connect(config.db_type, config.db_name)

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
        self.Classes        = Classes()
        self.Classes.Load()
        self.Config         = Cfg()
        self.Docs           = Docs()
        self.Docs.Load()
        self.DTDs           = DTDs()
        self.Formats        = Formats()
        self.Languages      = Languages()
        self.PubStatuses    = PubStatuses()
        self.ReviewStatuses = ReviewStatuses()
        self.Topics         = Topics()
        self.Users          = Users()

    def User(self, UserID):
        return User(UserID)

    def Doc(self, DocID):
        return Doc(DocID)


# Class

class Classes(LampadasCollection):
    """
    A collection object of all document classes (HOWTO, FAQ, etc).
    """
    
    def Load(self):
        sql = "SELECT class_id FROM class"
        self.cursor = db.select(sql)
        while (1):
            row = self.cursor.fetchone()
            if row == None: break
            newClass = Class()
            newClass.Load(row)
            self.data[newClass.ID] = newClass

class Class:
    """
    A class is a way of identifying the type of a document, such as a
    User's Guide, a HOWTO, or a FAQ List.
    """

    def __init__(self, ClassID=None):
        self.I18n = {}
        if ClassID==None: return
        self.ID = ClassID

    def Load(self, row):
        self.ID = row[0]
        sql = "SELECT lang, class_name, class_description FROM class_i18n WHERE class_id=" + str(self.ID)
        self.cursor = db.select(sql)
        while (1):
            self.row = self.cursor.fetchone()
            if self.row == None: break
            newClassI18n = ClassI18n()
            newClassI18n.Load(self.row)
            self.I18n[newClassI18n.Lang] = newClassI18n

class ClassI18n:
    """
    Holds localized strings that name and describe a class.
    """

    def Load(self, row):
        self.Lang		= row[0]
        self.Name		= trim(row[1])
        self.Description	= trim(row[2])

    
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
        self.sql = "SELECT name, value FROM config"
        self.cursor = db.select(self.sql)
        while (1):
            row = self.cursor.fetchone()
            if row == None: break
            self.data[trim(row[0])] = trim(row[1])


# Documents

class Docs(LampadasCollection):
    """
    A collection object providing access to all documents.
    """

    def Load(self):
        sql = "SELECT doc_id, title, class_id, format_id, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating, lang, sk_seriesid FROM document"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row == None: break
            newDoc = Doc()
            newDoc.LoadRow(row)
            self[newDoc.ID] = newDoc

# FIXME: try instantiating a new document, then adding *it* to the collection,
# rather than passing in all these parameters.

    def add(self, Title, ClassID, FormatID, DTD, DTDVersion, Version, LastUpdate, URL, ISBN, PubStatusCode, ReviewStatus, TickleDate, PubDate, HomeURL, TechReviewStatus, License, Abstract, Lang, SeriesID):
        self.id = db.read_value('SELECT max(doc_id) from document') + 1
        self.sql = "INSERT INTO document(doc_id, title, class_id, format_id, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, license, abstract, lang, sk_seriesid) VALUES (" + str(self.id) + ", " + wsq(Title) + ", " + str(ClassID) + ", " + dbint(FormatID) + ", " + wsq(DTD) + ", " + wsq(DTDVersion) + ", " + wsq(Version) + ", " + wsq(LastUpdate) + ", " + wsq(URL) + ", " + wsq(ISBN) + ", " + wsq(PubStatusCode) + ", " + wsq(ReviewStatus) + ", " + wsq(TickleDate) + ", " + wsq(PubDate) + ", " + wsq(HomeURL) + ", " + wsq(TechReviewStatus) + ", " + wsq(License) + ", " + wsq(Abstract) + ", " + wsq(Lang) + ", " + wsq(SeriesID) + ")"
        assert db.runsql(self.sql) == 1
        db.commit()
        self.NewID = db.read_value('SELECT MAX(doc_id) from document')
        newDoc = Doc(self.NewID)
        self[self.NewID] = newDoc
        return self.NewID
    
    def Del(self, id):
        self.sql = ('DELETE from document WHERE doc_id=' + str(id))
        assert db.runsql(self.sql) == 1
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
        sql = "SELECT doc_id, title, class_id, format_id, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating, lang, sk_seriesid FROM document WHERE doc_id=" + str(id)
        cursor = db.select(sql)
        row = cursor.fetchone()
        self.LoadRow(row)

    def LoadRow(self, row):
        self.ID			= row[0]
        #print "Loaded Doc ID: " + str(self.ID)
        self.Title		= trim(row[1])
        self.ClassID		= row[2]
        self.FormatID		= row[3]
        self.DTD		= trim(row[4])
        self.DTDVersion		= trim(row[5])
        self.Version		= trim(row[6])
        self.LastUpdate		= trim(row[7])
        self.URL		= trim(row[8])
        self.ISBN		= trim(row[9])
        self.PubStatusCode	= trim(row[10])
        self.ReviewStatus	= trim(row[11])
        self.TickleDate		= trim(row[12])
        self.PubDate		= trim(row[13])
        self.HomeURL		= trim(row[14])
        self.TechReviewStatus	= trim(row[15])
        self.Maintained		= tf2bool(row[16])
        self.License		= trim(row[17])
        self.Abstract		= trim(row[18])
        self.Rating		= safeint(row[19])
        self.Lang		= trim(row[20])
        self.SeriesID		= trim(row[21])

        self.Errs		= DocErrs(self.ID)
        self.Files		= DocFiles(self.ID)
        self.Ratings		= DocRatings(self.ID)
        self.Ratings.Parent	= self
        self.Versions		= DocVersions(self.ID)

    def Save(self):
        self.sql = "UPDATE document SET title=" + wsq(self.Title) + ", class_id=" + str(self.ClassID) + ", format_id=" + dbint(self.FormatID) + ", dtd=" + wsq(self.DTD) + ", dtd_version=" + wsq(self.DTDVersion) + ", version=" + wsq(self.Version) + ", last_update=" + wsq(self.LastUpdate) + ", url=" + wsq(self.URL) + ", isbn=" + wsq(self.ISBN) + ", pub_status=" + wsq(self.PubStatusCode) + ", review_status=" + wsq(self.ReviewStatus) + ", tickle_date=" + wsq(self.TickleDate) + ", pub_date=" + wsq(self.PubDate) + ", ref_url=" + wsq(self.HomeURL) + ", tech_review_status=" + wsq(self.TechReviewStatus) + ", maintained=" + wsq(bool2tf(self.Maintained)) + ", license=" + wsq(self.License) + ", abstract=" + wsq(self.Abstract) + ", rating=" + dbint(self.Rating) + ", lang=" + wsq(self.Lang) + ", sk_seriesid=" + wsq(self.SeriesID) + " WHERE doc_id=" + str(self.ID)
        db.runsql(self.sql)
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
        self.sql = "SELECT err_id FROM document_error WHERE doc_id=" + str(DocID)
        self.cursor = db.select(self.sql)
        while (1):
            row = self.cursor.fetchone()
            if row == None: break
            newDocErr = DocErr()
            newDocErr.Load(DocID, row)
            self.list = self.list + [newDocErr]

    def Clear(self):
        self.sql = "DELETE FROM document_error WHERE doc_id=" + str(self.DocID)
        db.runsql(self.sql)
        db.commit()
        self.list = []

# FIXME: Try instantiating a DocErr object, then adding it to the *document*
# rather than passing all these parameters here.

    def add(self, ErrID):
        self.sql = "INSERT INTO document_error(doc_id, err_id) VALUES (" + str(self.DocID) + ", " + wsq(ErrID)
        assert db.runsql(self.sql) == 1
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
        self.sql = "SELECT filename, format_id FROM document_file WHERE doc_id=" + str(DocID)
        self.cursor = db.select(self.sql)
        while (1):
            row = self.cursor.fetchone()
            if row == None: break
            newDocFile = DocFile()
            newDocFile.Load(DocID, row)
            self.data[newDocFile.Filename] = newDocFile

    def add(self, DocID, Filename, FormatID=None):
        self.sql = 'INSERT INTO document_file (doc_id, filename, format_id) VALUES (' + str(DocID) + ', ' + wsq(Filename) + ', ' + dbint(FormatID) + ')'
        assert db.runsql(self.sql) == 1
        db.commit()
        newDocFile = DocFile()
        newDocFile.DocID = DocID
        newDocFile.Filename = Filename
        newDocFile.FormatID = FormatID
        
    def Clear(self):
        self.sql = "DELETE FROM document_file WHERE doc_id=" + str(self.DocID)
        db.runsql(self.sql)
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
        self.sql = "UPDATE document_file SET format_id=" + dbint(self.FormatID) + " WHERE doc_id=" + str(self.DocID) + " AND filename=" + wsq(self.Filename)
        db.runsql(self.sql)
        db.commit()

    def Del(self):
        self.sql = "DELETE FROM document_file WHERE doc_id=" + str(self.DocID) + " AND filename=" + wsq(self.Filename)
        db.runsql(self.sql)
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
        self.sql = "SELECT user_id, date_entered, vote FROM doc_vote WHERE doc_id=" + str(DocID)
        self.cursor = db.select(self.sql)
        while (1):
            self.row = self.cursor.fetchone()
            if self.row == None: break
            newDocRating = DocRating()
            newDocRating.Load(DocID, self.row)
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
        self.sql = 'DELETE FROM doc_vote WHERE doc_id=' + str(self.DocID) + ' AND user_id=' + str(UserID)
        db.runsql(self.sql)
        self.CalcAverage()
        
    def Clear(self):
        self.sql = "DELETE FROM doc_vote WHERE doc_id=" + str(self.DocID)
        db.runsql(self.sql)
        self.data = {}
        self.CalcAverage()

    def CalcAverage(self):
        self.Average = 0
        if self.count() > 0:
            keys = self.data.keys()
            for key in keys:
                self.Average = self.Average + self.data[key].Rating
            self.Average = self.Average / self.count()
        self.sql = "UPDATE document SET rating=" + str(self.Average) + " WHERE doc_id=" + str(self.DocID)
#		db.runsql(self.sql)
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
        self.sql = "DELETE from doc_vote WHERE doc_id=" + str(self.DocID) + " AND user_id=" + str(self.UserID)
        db.runsql(self.sql)
        self.sql = "INSERT INTO doc_vote (doc_id, user_id, vote) VALUES (" + str(self.DocID) + ", " + str(self.UserID) + ", " + str(self.Rating) + ")"
        db.runsql(self.sql)
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
        self.sql = "SELECT rev_id, version, pub_date, initials, notes FROM document_rev WHERE doc_id=" + str(DocID)
        self.cursor = db.select(self.sql)
        while (1):
            self.row = self.cursor.fetchone()
            if self.row == None: break
            newDocVersion = DocVersion()
            newDocVersion.Load(DocID, self.row)
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
        self.PubDate	= trim(row[2])
        self.Initials	= trim(row[3])
        self.Notes	= trim(row[4])

    def Save(self):
        self.sql = "UPDATE document_rev SET version=" + wsq(self.Version) + ", pub_date=" + wsq(self.PubDate) + ", initials=" + wsq(self.Initials) + ", notes=" + wsq(self.Notes) + "WHERE doc_id=" + str(self.DocID) + " AND rev_id" + wsq(self.ID)
        assert db.runsql(self.sql) == 1
        db.commit()


# DTDs

class DTDs(LampadasCollection):
    """
    A collection object of all DTDs.
    """
    
    def __init__(self):
        self.data = {}
        self.sql = "SELECT dtd from dtd"
        self.cursor = db.select(self.sql)
        while (1):
            row = self.cursor.fetchone()
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
        self.sql = "SELECT err_id FROM error"
        self.cursor = db.select(self.sql)
        while (1):
            row = self.cursor.fetchone()
            if row == None: break
            newErr = Err()
            newErr.Load(row)
            self.data[newErr.ErrID] = newErr

class Err:
    """
    An error that can be filed against a document.
    """
    
    def __init__(self, ErrID=None):
        self.I18n = {}
        if Err==None: return
        self.ErrID = ErrID

    def Load(self, row):
        self.ErrID = trim(row[0])
        self.sql = "SELECT lang, err_name, err_desc FROM error_i18n WHERE err_id=" + wsq(self.ErrID)
        self.cursor = db.select(self.sql)
        while (1):
            self.row = self.cursor.fetchone()
            if self.row == None: break
            newErrI18n = ErrI18n()
            newErrI18n.Load(self.row)
            self.I18n[newErrI18n.Lang] = newErrI18n

# ErrI18n

class ErrI18n:

    def Load(self, row):
        self.Lang		= row[0]
        self.Name		= trim(row[1])
        self.Description	= trim(row[1])


# Formats

class Formats(LampadasCollection):
    """
    A collection object of all formats.
    """
    
    def __init__(self):
        self.data = {}
        self.sql = "SELECT format_id FROM format"
        self.cursor = db.select(self.sql)
        while (1):
            row = self.cursor.fetchone()
            if row == None: break
            newFormat = Format()
            newFormat.Load(row)
            self.data[newFormat.ID] = newFormat

class Format:
    """
    A file format, for document source files.
    """

    def __init__(self, FormatID=None):
        self.I18n = {}
        if FormatID==None: return
        self.ID = FormatID

    def Load(self, row):
        self.ID = row[0]
        self.sql = "SELECT lang, format_name, format_desc FROM format_i18n WHERE format_id=" + str(self.ID)
        self.cursor = db.select(self.sql)
        while (1):
            self.row = self.cursor.fetchone()
            if self.row == None: break
            newFormatI18n = FormatI18n()
            newFormatI18n.Load(self.row)
            self.I18n[newFormatI18n.Lang] = newFormatI18n

# FormatI18n

class FormatI18n:

    def Load(self, row):
        self.Lang		= row[0]
        self.Name		= trim(row[1])
        self.Description	= trim(row[2])


# Languages

class Languages(LampadasCollection):
    """
    A collection object of all languages supported by the ISO 639
    standard.
    """

    def __init__(self):
        self.data = {}
        self.sql = "SELECT isocode, supported FROM language"
        self.cursor = db.select(self.sql)
        while (1):
            row = self.cursor.fetchone()
            if row == None: break
            newLanguage = Language()
            newLanguage.Load(row)
            self.data[newLanguage.Code] = newLanguage

class Language:
    """
    Defines a language supported by Lampadas. Documents can be translated into,
    and Lampadas can be localized for, any language supported by ISO 639.
    """

    def __init__(self, LanguageCode=None):
        self.I18n = {}
        if LanguageCode == None: return
        self.Code = LanguageCode
        self.sql = "SELECT isocode, supported FROM language WHERE isocode= " + wsq(LanguageCode)
        self.cursor = db.select(self.sql)
        self.Load(self.sql)

    def Load(self, row):
        self.Code	= trim(row[0])
        self.Supported	= tf2bool(row[1])
        self.sql = "SELECT lang, language_name FROM language_i18n WHERE isocode=" + wsq(self.Code)
        self.cursor = db.select(self.sql)
        while (1):
            self.row = self.cursor.fetchone()
            if self.row == None: break
            newLanguageI18n = LanguageI18n()
            newLanguageI18n.Load(self.row)
            self.I18n[newLanguageI18n.Lang] = newLanguageI18n

# LanguageI18n

class LanguageI18n:

    def Load(self, row):
        self.Lang		= row[0]
        self.Name		= trim(row[1])


# PubStatuses

class PubStatuses(LampadasCollection):
    """
    A collection object of all publication statuses.
    """
    
    def __init__(self):
        self.data = {}
        self.sql = "SELECT pub_status FROM pub_status"
        self.cursor = db.select(self.sql)
        while (1):
            row = self.cursor.fetchone()
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
        self.I18n = {}
        if PubStatusCode==None: return
        self.Code = PubStatusCode

    def Load(self, row):
        self.Code = trim(row[0])
        self.sql = "SELECT lang, pub_status_name, pub_status_desc FROM pub_status_i18n WHERE pub_status=" + wsq(self.Code)
        self.cursor = db.select(self.sql)
        while (1):
            self.row = self.cursor.fetchone()
            if self.row == None: break
            newPubStatusI18n = PubStatusI18n()
            newPubStatusI18n.Load(self.row)
            self.I18n[newPubStatusI18n.Lang] = newPubStatusI18n

# PubStatusI18n

class PubStatusI18n:

    def Load(self, row):
        self.Lang		= row[0]
        self.Name		= trim(row[1])
        self.Description	= trim(row[2])


# ReviewStatuses

class ReviewStatuses(LampadasCollection):
    """
    A collection object of all publication statuses.
    """
    
    def __init__(self):
        self.data = {}
        self.sql = "SELECT review_status FROM review_status"
        self.cursor = db.select(self.sql)
        while (1):
            row = self.cursor.fetchone()
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
        self.I18n = {}
        if ReviewStatusCode==None: return
        self.Code = ReviewStatusCode

    def Load(self, row):
        self.Code = trim(row[0])
        self.sql = "SELECT lang, review_status_name, review_status_desc FROM review_status_i18n WHERE review_status=" + wsq(self.Code)
        self.cursor = db.select(self.sql)
        while (1):
            self.row = self.cursor.fetchone()
            if self.row == None: break
            newReviewStatusI18n = ReviewStatusI18n()
            newReviewStatusI18n.Load(self.row)
            self.I18n[newReviewStatusI18n.Lang] = newReviewStatusI18n

# ReviewStatusI18n

class ReviewStatusI18n:

    def Load(self, row):
        self.Lang		= row[0]
        self.Name		= trim(row[1])
        self.Description	= trim(row[2])


# Topics

class Topics(LampadasCollection):
    """
    A collection object of all topics.
    """
    
    def __init__(self):
        self.data = {}
        self.sql = "SELECT topic_num FROM topic"
        self.cursor = db.select(self.sql)
        while (1):
            row = self.cursor.fetchone()
            if row == None: break
            newTopic = Topic()
            newTopic.Load(row)
            self.data[newTopic.Num] = newTopic

class Topic:
    """
    Each document can be assigned an arbitrary number of topics.
    The web interface allows a user to browse through document topics,
    to help them find a document on the subject in which they are interested.
    """

    def __init__(self, TopicNum=None):
        self.I18n = {}
        if TopicNum==None: return
        self.Num = TopicNum

    def Load(self, row):
        self.Num = trim(row[0])
        self.sql = "SELECT lang, topic_name, topic_description FROM topic_i18n string_i18n WHERE topic_num=" + wsq(self.Num)
        self.cursor = db.select(self.sql)
        while (1):
            self.row = self.cursor.fetchone()
            if self.row == None: break
            newTopicI18n = TopicI18n()
            newTopicI18n.Load(self.row)
            self.I18n[newTopicI18n.Lang] = newTopicI18n

class TopicI18n:

    def Load(self, row):
        self.Lang		= row[0]
        self.Name		= trim(row[1])
        self.Description	= trim(row[2])

    
# Users

class Users:
    """
    A collection object providing access to registered users.
    """

    def count(self):
        return db.read_value('SELECT count(*) from username')

    def add(self, Username, FirstName, MiddleName, Surname, Email, IsAdmin, IsSysadmin, Password, Notes, Stylesheet):
        self.id = db.read_value('SELECT max(user_id) from username') + 1
        self.sql = "INSERT INTO username (user_id, username, first_name, middle_name, surname, email, admin, sysadmin, password, notes, stylesheet) VALUES (" + str(self.id) + ", " + wsq(Username) + ", " + wsq(FirstName) + ", " + wsq(MiddleName) + ", " + wsq(Surname) + ", " + wsq(Email) + ", " + wsq(bool2tf(IsAdmin)) + ", " + wsq(bool2tf(IsSysadmin)) + ", " + wsq(Password) + ", " + wsq(Notes) + ", " + wsq(Stylesheet) + ")"
        assert db.runsql(self.sql) == 1
        db.commit()
        return db.read_value('SELECT max(user_id) from username')
    
    def Del(self, id):
        self.sql = ('DELETE from username WHERE user_id=' + str(id))
        assert db.runsql(self.sql) == 1
        db.commit()

class User:
    """
    A user is known by the system and can login to manipulate documents
    and act on the database according to his rights.
    """

    def __init__(self, id) :
        self.sql = 'SELECT user_id, username, session_id, first_name, middle_name, surname, email, admin, sysadmin, password, notes, stylesheet FROM username WHERE user_id=' + str(id)
        self.cursor = db.select(self.sql)
        row = self.cursor.fetchone()
        self.ID		= row[0]
        self.Username	= trim(row[1])
        self.SessionID	= trim(row[2])
        self.FirstName	= trim(row[3])
        self.MiddleName	= trim(row[4])
        self.Surname	= trim(row[5])
        self.Email	= trim(row[6])
        self.IsAdmin	= tf2bool(row[7])
        self.IsSyadmin	= tf2bool(row[8])
        self.Password	= trim(row[9])
        self.Notes	= trim(row[10])
        self.Stylesheet	= trim(row[11])
        self.Name	= trim(trim(self.FirstName + ' ' + self.MiddleName) + ' ' + self.Surname)

        self.Docs = UserDocs(self.ID)


# UserDocs

class UserDocs(LampadasList):
    """
    A collection object providing access to all user document associations.
    """

    def __init__(self, UserID):
        #print "Loading user docs for user: " + str(UserID)
        LampadasList.__init__(self)
        assert not UserID == None
        self.UserID = UserID
        sql = "SELECT doc_id, user_id, role, email, active FROM document_user WHERE user_id=" + str(self.UserID)
        cursor = db.select(sql)
        #print sql
        while (1):
            #print "Loading UserDocs row"
            row = cursor.fetchone()
            if row == None: break
            #print "Loaded UserDocs row"
            newUserDoc = UserDoc(row[0], UserID)
            self.list = self.list + [newUserDoc]

    def add(self, DocID, Role, Email, Active):
        sql = "INSERT INTO document_user(doc_id, user_id, role, email, active) VALUES (" + str(DocID) + ", " + str(self.UserID) + ", " + wsq(Role) + ", " + wsq(Email) + ", " + wsq(bool2tf(Active)) +  " )"
        assert db.runsql(sql) == 1
        db.commit()
    
    def Del(self, DocID):
        sql = ('DELETE from document_user WHERE doc_id=' + str(DocID) + ' AND user_id=' + str(self.UserID))
        assert db.runsql(sql) == 1
        db.commit()
        del self.col[DocID]

class UserDoc(Doc):
    """
    An association between a user and a document. This association defines the role
    which the user plays in the production of the document.
    """

    def __init__(self, DocID=None, UserID=None):
        #print "initializing UserDoc, DocID: " + str(DocID) + ", UserID: " + str(UserID)
        Doc.__init__(self, DocID)
        self.DocID = DocID
        self.UserID = UserID
        #print "UserDoc.UserID: " + str(UserID)
        if DocID == None: return
        if UserID == None: return
        #print "Calling UserDoc.load"
        self.Load(DocID, UserID)

    def Load(self, DocID=None, UserID=None):
        #print "Loading UserDoc, DocID: " + str(DocID) + ", UserID: " + str(UserID)
        if not DocID == None:
            self.DocID = DocID
        assert not self.DocID == None
        if not UserID == None:
            self.UserID = UserID
        assert not self.UserID == None
        sql = "SELECT doc_id, user_id, role, email, active FROM document_user WHERE doc_id=" + str(self.DocID) + " AND user_id=" + str(self.UserID)
        cursor = db.select(sql)
        row = cursor.fetchone()
        self.LoadRow(row)
        Doc.Load(self, self.DocID)

    def LoadRow(self, row):
        assert not row == None
        self.DocID		= row[0]
        self.UserID		= row[1]
        self.Role		= trim(row[2])
        self.Email		= trim(row[3])
        self.Active		= tf2bool(row[4])

    def Save(self):
        sql = "UPDATE document_user SET role=" + wsq(self.Role) + ", email=" + wsq(self.Email) + ", active=" + wsq(bool2tf(self.Active)) + " WHERE doc_id=" + str(self.DocID) + " AND user_id=" + str(self.UserID)
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
    
