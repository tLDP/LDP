#!/usr/bin/python

"""
Lampadas Object Hierarchy Module

This module defines Data Objects (Users, Documents, Notes, Topics, etc.)
for the Lampadas system. All access to the underlying database should be
performed through this layer.
"""

# Modules

import Config
import Database
import Log
from string import strip
from types import StringType
#from UserDict import UserDict


# Globals

Config = Config.Config()
DB = Database.Database()
DB.Connect(Config.DBType, Config.DBName)
Log = Log.Log()
Log.Truncate()


# Base Classes

class LampadasList:
	"""
	Base class for Lampadas list objects, which are cached in RAM
	for high performance.

	Classes based on this one emulate lists, with additional methods.
	"""

	list = []

	def __len__(self):
		return len(self.list)

	def __getitem__(self, key):
		return self.list[key]

	def __setitem__(self, key, value):
		self.list[key] = value
	
	def __delitem__(self, key):
		del self.list[key]

	def items(self):
		return self.list.items()

	def append(self, item):
		self.list.append(item)
		
	def Count(self):
		return len(self.list)


class LampadasCollection:
	"""
	Base class for Lampadas collection objects, which are cached in RAM
	for high performance.

	Classes based on this one become pseudo-dictionaries, providing
	iteration and similar methods. This is done by providing a wrapper to
	the built-in dictionary type. In Python 2.2, dictionaries will be
	subclassable, so this can be rewritten to take advantage of that.
	"""

	def __init__(self):
		self.data = {}

	def __getitem__(self, key):
		try:
			item = self.data[key]
		except KeyError:
			item = None
		return item

	def __setitem__(self, key, item):
		self.data[key] = item

	def __delitem__(self, key):
		del self.data[key]

	def keys(self):
		return self.data.keys()

	def Count(self):
		return len(self.data)


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
		self.Classes	= Classes()
		self.Classes.Load()
		self.Config	= Config()
		self.Config.Load()
		self.Docs	= Docs()
		self.Docs.Load()
		self.Strings	= Strings()
		self.Users	= Users()


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
		self.sql = "SELECT class_id FROM class"
		self.cursor = DB.Select(self.sql)
		while (1):
			row = self.cursor.fetchone()
			if row == None: break
			newClass = Class()
			newClass.Load(row)
			self.data[newClass.ID] = newClass

#	def Add(self, Title, ClassID, Format, DTD, DTDVersion, Version, LastUpdate, URL, ISBN, PubStatus, ReviewStatus, TickleDate, PubDate, HomeURL, TechReviewStatus, License, Abstract, LanguageCode, SeriesID):
#		self.id = DB.Value('SELECT max(doc_id) from document') + 1
#		self.sql = "INSERT INTO document(doc_id, title, class_id, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, license, abstract, lang, sk_seriesid) VALUES (" + str(self.id) + ", " + wsq(Title) + ", " + str(ClassID) + ", " + wsq(Format) + ", " + wsq(DTD) + ", " + wsq(DTDVersion) + ", " + wsq(Version) + ", " + wsq(LastUpdate) + ", " + wsq(URL) + ", " + wsq(ISBN) + ", " + wsq(PubStatus) + ", " + wsq(ReviewStatus) + ", " + wsq(TickleDate) + ", " + wsq(PubDate) + ", " + wsq(HomeURL) + ", " + wsq(TechReviewStatus) + ", " + wsq(License) + ", " + wsq(Abstract) + ", " + wsq(LanguageCode) + ", " + wsq(SeriesID) + ")"
#		assert DB.Exec(self.sql) == 1
#		DB.Commit()
#		self.NewID = DB.Value('SELECT MAX(doc_id) from document')
#		newDoc = Doc(self.NewID)
#		self[self.NewID] = newDoc
#		return self.NewID
	
#	def Del(self, id):
#		self.sql = ('DELETE from document WHERE doc_id=' + str(id))
#		assert DB.Exec(self.sql) == 1
#		DB.Commit()
#		del self[id]



class Class:

	def __init__(self, ClassID=None):
		self.I18n = {}
		if ClassID==None: return
		self.ID = ClassID

	def Load(self, row):
		self.ID = row[0]
		self.sql = "SELECT lang, class_name, class_description FROM class_i18n WHERE class_id=" + str(self.ID)
		self.cursor = DB.Select(self.sql)
		while (1):
			self.row = self.cursor.fetchone()
			if self.row == None: break
			newClassI18n = ClassI18n()
			newClassI18n.Load(self.row)
			self.I18n[newClassI18n.Lang] = newClassI18n

# ClassI18n

class ClassI18n:

	def Load(self, row):
		self.Lang		= row[0]
		self.Name		= trim(row[1])
		self.Description	= trim(row[2])

	
# Config

class Config(LampadasCollection):

	def Load(self):
		self.sql = "SELECT name, value FROM config"
		self.cursor = DB.Select(self.sql)
		while (1):
			row = self.cursor.fetchone()
			if row == None: break
			self[trim(row[0])] = trim(row[1])
		


# Documents

class Docs(LampadasCollection):
	"""
	A collection object providing access to all documents.
	"""

	def Load(self):
		self.sql = "SELECT doc_id, title, class_id, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating, lang, sk_seriesid FROM document"
		self.cursor = DB.Select(self.sql)
		while (1):
			row = self.cursor.fetchone()
			if row == None: break
			newDoc = Doc()
			newDoc.Load(row)
			self[newDoc.ID] = newDoc

	def Add(self, Title, ClassID, Format, DTD, DTDVersion, Version, LastUpdate, URL, ISBN, PubStatus, ReviewStatus, TickleDate, PubDate, HomeURL, TechReviewStatus, License, Abstract, LanguageCode, SeriesID):
		self.id = DB.Value('SELECT max(doc_id) from document') + 1
		self.sql = "INSERT INTO document(doc_id, title, class_id, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, license, abstract, lang, sk_seriesid) VALUES (" + str(self.id) + ", " + wsq(Title) + ", " + str(ClassID) + ", " + wsq(Format) + ", " + wsq(DTD) + ", " + wsq(DTDVersion) + ", " + wsq(Version) + ", " + wsq(LastUpdate) + ", " + wsq(URL) + ", " + wsq(ISBN) + ", " + wsq(PubStatus) + ", " + wsq(ReviewStatus) + ", " + wsq(TickleDate) + ", " + wsq(PubDate) + ", " + wsq(HomeURL) + ", " + wsq(TechReviewStatus) + ", " + wsq(License) + ", " + wsq(Abstract) + ", " + wsq(LanguageCode) + ", " + wsq(SeriesID) + ")"
		assert DB.Exec(self.sql) == 1
		DB.Commit()
		self.NewID = DB.Value('SELECT MAX(doc_id) from document')
		newDoc = Doc(self.NewID)
		self[self.NewID] = newDoc
		return self.NewID
	
	def Del(self, id):
		self.sql = ('DELETE from document WHERE doc_id=' + str(id))
		assert DB.Exec(self.sql) == 1
		DB.Commit()
		del self[id]


class Doc:
	"""
	A document in any format, whether local or remote.
	"""

	def __init__(self, id=None):
		if id == None: return
		self.sql = "SELECT doc_id, title, class_id, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating, lang, sk_seriesid FROM document WHERE doc_id=" + str(id)
		self.cursor = DB.Select(self.sql)
		row = self.cursor.fetchone()
		self.Load(row)

	def Load(self, row):
		self.ID			= row[0]
		self.Title		= trim(row[1])
		self.ClassID		= row[2]
		self.Format		= trim(row[3])
		self.DTD		= trim(row[4])
		self.DTDVersion		= trim(row[5])
		self.Version		= trim(row[6])
		self.LastUpdate		= trim(row[7])
		self.URL		= trim(row[8])
		self.ISBN		= trim(row[9])
		self.PubStatus		= trim(row[10])
		self.ReviewStatus	= trim(row[11])
		self.TickleDate		= trim(row[12])
		self.PubDate		= trim(row[13])
		self.HomeURL		= trim(row[14])
		self.TechReviewStatus	= trim(row[15])
		self.Maintained		= tf2bool(row[16])
		self.License		= trim(row[17])
		self.Abstract		= trim(row[18])
		self.Rating		= row[19]
		self.LanguageCode	= trim(row[20])
		self.SeriesID		= trim(row[21])

		self.Files		= DocFiles(self.ID)
		self.Errors		= DocErrors(self.ID)

	def Save(self):
		self.sql = "UPDATE document SET title=" + wsq(self.Title) + ", class_id=" + str(self.ClassID) + ", format=" + wsq(self.Format) + ", dtd=" + wsq(self.DTD) + ", dtd_version=" + wsq(self.DTDVersion) + ", version=" + wsq(self.Version) + ", last_update=" + wsq(self.LastUpdate) + ", url=" + wsq(self.URL) + ", isbn=" + wsq(self.ISBN) + ", pub_status=" + wsq(self.PubStatus) + ", review_status=" + wsq(self.ReviewStatus) + ", tickle_date=" + wsq(self.TickleDate) + ", pub_date=" + wsq(self.PubDate) + ", ref_url=" + wsq(self.HomeURL) + ", tech_review_status=" + wsq(self.TechReviewStatus) + ", maintained=" + wsq(bool2tf(self.Maintained)) + ", license=" + wsq(self.License) + ", abstract=" + wsq(self.Abstract) + ", rating=" + wsq(self.Rating) + ", lang=" + wsq(self.LanguageCode) + ", sk_seriesid=" + wsq(self.SeriesID) + " WHERE doc_id=" + str(self.ID)
		DB.Exec(self.sql)
		DB.Commit()


# DocFiles

class DocFiles(LampadasCollection):
	"""
	A collection object providing access to all document source files.
	"""

	def __init__(self, DocID):
		self.data = {}
		assert not DocID == None
		self.DocID = DocID
		self.sql = "SELECT filename, format FROM document_file WHERE doc_id=" + str(DocID)
		self.cursor = DB.Select(self.sql)
		while (1):
			row = self.cursor.fetchone()
			if row == None: break
			newDocFile = DocFile()
			newDocFile.Load(DocID, row)
			self.data[newDocFile.Filename] = newDocFile


class DocFile:
	"""
	An association between a document and a file.
	"""

	def Load(self, DocID, row):
		assert not DocID == None
		assert not row == None
		self.DocID	= DocID
		self.Filename	= trim(row[0])
		self.Format	= trim(row[1])

	def Save(self):
		self.sql = "UPDATE document_file SET format=" + wsq(self.Format) + " WHERE doc_id=" + str(self.DocID) + " AND filename=" + wsq(self.Filename)
		assert DB.Exec(self.sql) == 1
		DB.Commit()
		


# DocErrors

class DocErrors(LampadasList):
	"""
	A collection object providing access to all document errors, as identified by the
	Lintadas subsystem.
	"""

	def __init__(self, DocID):
		assert not DocID == None
		self.DocID = DocID
		self.sql = "SELECT error FROM document_error WHERE doc_id=" + str(DocID)
		self.cursor = DB.Select(self.sql)
		while (1):
			row = self.cursor.fetchone()
			if row == None: break
			newDocError = DocError()
			newDocError.Load(DocID, row)
			self.list = self.list + [newDocError]

	def Clear(self):
		self.sql = "DELETE FROM document_error WHERE doc_id=" + str(self.DocID)
		DB.Exec(self.sql)
		self.list = []

	def Add(self, Error):
		self.sql = "INSERT INTO document_error(doc_id, error) VALUES (" + str(self.DocID) + ", " + wsq(Error)
		assert DB.Exec(self.sql) == 1
		newDocError = DocError()
		newDocError.DocID = self.DocID
		newDocError.Error = Error
		self.list = self.list + [newDocError]
		

class DocError:
	"""
	An error filed against a document by the Lintadas subsystem.
	"""

	def Load(self, DocID, row):
		assert not DocID == None
		assert not row == None
		self.DocID	= DocID
		self.Error	= trim(row[0])


# String

class Strings(LampadasCollection):
	"""
	A collection object of all localized strings.
	"""
	
	def __init__(self):
		self.data = {}
		self.sql = "SELECT string_code FROM string"
		self.cursor = DB.Select(self.sql)
		while (1):
			row = self.cursor.fetchone()
			if row == None: break
			newString = String()
			newString.Load(row)
			self.data[newString.Code] = newString

#	def Add(self, Title, StringID, Format, DTD, DTDVersion, Version, LastUpdate, URL, ISBN, PubStatus, ReviewStatus, TickleDate, PubDate, HomeURL, TechReviewStatus, License, Abstract, LanguageCode, SeriesID):
#		self.id = DB.Value('SELECT max(doc_id) from document') + 1
#		self.sql = "INSERT INTO document(doc_id, title, class_id, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, license, abstract, lang, sk_seriesid) VALUES (" + str(self.id) + ", " + wsq(Title) + ", " + str(StringID) + ", " + wsq(Format) + ", " + wsq(DTD) + ", " + wsq(DTDVersion) + ", " + wsq(Version) + ", " + wsq(LastUpdate) + ", " + wsq(URL) + ", " + wsq(ISBN) + ", " + wsq(PubStatus) + ", " + wsq(ReviewStatus) + ", " + wsq(TickleDate) + ", " + wsq(PubDate) + ", " + wsq(HomeURL) + ", " + wsq(TechReviewStatus) + ", " + wsq(License) + ", " + wsq(Abstract) + ", " + wsq(LanguageCode) + ", " + wsq(SeriesID) + ")"
#		assert DB.Exec(self.sql) == 1
#		DB.Commit()
#		self.NewID = DB.Value('SELECT MAX(doc_id) from document')
#		newDoc = Doc(self.NewID)
#		self[self.NewID] = newDoc
#		return self.NewID
	
#	def Del(self, id):
#		self.sql = ('DELETE from document WHERE doc_id=' + str(id))
#		assert DB.Exec(self.sql) == 1
#		DB.Commit()
#		del self[id]



class String:

	def __init__(self, StringCode=None):
		self.I18n = {}
		if StringCode==None: return
		self.Code = StringCode

	def Load(self, row):
		self.Code = trim(row[0])
		self.sql = "SELECT lang, string FROM string_i18n WHERE string_code=" + wsq(self.Code)
		self.cursor = DB.Select(self.sql)
		while (1):
			self.row = self.cursor.fetchone()
			if self.row == None: break
			newStringI18n = StringI18n()
			newStringI18n.Load(self.row)
			self.I18n[newStringI18n.Lang] = newStringI18n

# StringI18n

class StringI18n:

	def Load(self, row):
		self.Lang		= row[0]
		self.Text		= trim(row[1])

	
# Users

class Users:
	"""
	A collection object providing access to registered users.
	"""

	def Count(self):
		return DB.Value('SELECT count(*) from username')

	def Add(self, Username, FirstName, MiddleName, Surname, Email, IsAdmin, IsSysadmin, Password, Notes, Stylesheet):
		self.id = DB.Value('SELECT max(user_id) from username') + 1
		self.sql = "INSERT INTO username (user_id, username, first_name, middle_name, surname, email, admin, sysadmin, password, notes, stylesheet) VALUES (" + str(self.id) + ", " + wsq(Username) + ", " + wsq(FirstName) + ", " + wsq(MiddleName) + ", " + wsq(Surname) + ", " + wsq(Email) + ", " + wsq(bool2tf(IsAdmin)) + ", " + wsq(bool2tf(IsSysadmin)) + ", " + wsq(Password) + ", " + wsq(Notes) + ", " + wsq(Stylesheet) + ")"
		assert DB.Exec(self.sql) == 1
		DB.Commit()
		return DB.Value('SELECT max(user_id) from username')
	
	def Del(self, id):
		self.sql = ('DELETE from username WHERE user_id=' + str(id))
		assert DB.Exec(self.sql) == 1
		DB.Commit()

class User:
	"""
	A user is known by the system and can login to manipulate documents
	and act on the database according to his rights.
	"""

	def __init__(self, id) :
		self.sql = 'SELECT user_id, username, session_id, first_name, middle_name, surname, email, admin, sysadmin, password, notes, stylesheet FROM username WHERE user_id=' + str(id)
		self.cursor = DB.Select(self.sql)
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
		assert not UserID == None
		self.UserID = UserID
		self.sql = "SELECT doc_id, user_id, role, email, active FROM document_user WHERE user_id=" + str(self.UserID)
		self.cursor = DB.Select(self.sql)
		while (1):
			row = self.cursor.fetchone()
			if row == None: break
			newUserDoc = UserDoc(UserID, row[0])
			newUserDoc.Load(row)
			self.list = self.list + [newUserDoc]

	def Add(self, DocID, Role, Email, Active):
		self.sql = "INSERT INTO document_user(doc_id, user_id, role, email, active) VALUES (" + str(DocID) + ", " + str(self.UserID) + ", " + wsq(Role) + ", " + wsq(Email) + ", " + wsq(bool2tf(Active)) +  " )"
		assert DB.Exec(self.sql) == 1
		DB.Commit()
	
	def Del(self, DocID):
		self.sql = ('DELETE from document_user WHERE doc_id=' + str(DocID) + ' AND user_id=' + str(self.UserID))
		assert DB.Exec(self.sql) == 1
		DB.Commit()
		del self.col[DocID]


class UserDoc:
	"""
	An association between a user and a document.
	"""

	def __init__(self, UserID=None, DocID=None):
		self.UserID = UserID
		self.DocID = DocID
		if DocID == None: return
		if UserID == None: return
		self.sql = "SELECT doc_id, user_id, role, email, active FROM document_user WHERE doc_id=" + str(DocID) + " AND user_id=" + str(UserID)
		self.cursor = DB.Select(self.sql)
		row = self.cursor.fetchone()
		self.Load(row)

	def Load(self, row):
		assert not row == None
		self.DocID		= row[0]
		self.UserID		= row[1]
		self.Role		= trim(row[2])
		self.Email		= trim(row[3])
		self.Active		= tf2bool(row[4])

	def Save(self):
		self.sql = "UPDATE document_user SET role=" + wsq(self.Role) + ", email=" + wsq(self.Email) + ", active=" + wsq(bool2tf(self.Active)) + " WHERE doc_id=" + str(self.DocID) + " AND user_id=" + str(self.UserID)
		DB.Exec(self.sql)
		DB.Commit()



	

# Utility routines

def wsq(astring):
	if astring == None:
		return 'NULL'
	elif astring == '':
		return 'NULL'
	else:
		return "'" + astring.replace("'", "''") + "'"

def bool2tf(bool):
	if bool == 1:
		return 't'
	else:
		return 'f'

def tf2bool(tf):
	if tf == 't':
		return 1
	else:
		return 0

def trim(astring):
	if astring == None:
		temp = ''
	else:
		temp = str(astring)
	return strip(temp)

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
	
