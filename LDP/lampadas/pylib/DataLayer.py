#!/usr/bin/python

"""
Lampadas Object Hierarchy Module

This module defines Data Objects (Users, Documents, Notes, Topics, etc.)
for the Lampadas system. All access to the underlying database should be
performed through this layer.
"""

# Modules ##################################################################

import Config
import Database
from string import strip
from types import StringType

Config = Config.Config()
DB = Database.Database()
DB.Connect(Config.DBType, Config.DBName)

class LampadasList:
	"""
	Base class for Lampadas list objects, which are cached in RAM
	for high performance.

	Classes based on this one emulast lists, with additional methods.
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

	def keys(self):
		return self.list.keys()

	def items(self):
		return self.list.items()

	def append(self, item):
		self.list.append(item)
		
	def Count(self):
		return len(data)


class LampadasCollection:
	"""
	Base class for Lampadas collection objects, which are cached in RAM
	for high performance.

	Classes based on this one become pseudo-dictionaries, providing
	iteration and similar methods. This is done by providing a wrapper to
	the built-in dictionary type. In Python 2.2, dictionaries will be
	subclassable, so this can be rewritten to take advantage of that.
	"""

	col = {}

	def __getitem__(self, id):
		return self.col[id]
	
	def Count(self):
		return len(self.col)


# Users

class Users:
	"""
	A collection object providing access to registered users.
	"""

	def Count(self):
		return DB.Value('select count(*) from username')

	def Add(self, Username, FirstName, MiddleName, Surname, Email, IsAdmin, IsSysadmin, Password, Notes, Stylesheet):
		self.id = DB.Value('select max(user_id) from username') + 1
		self.sql = "INSERT INTO username (user_id, username, first_name, middle_name, surname, email, admin, sysadmin, password, notes, stylesheet) VALUES (" + str(self.id) + ", " + wsq(Username) + ", " + wsq(FirstName) + ", " + wsq(MiddleName) + ", " + wsq(Surname) + ", " + wsq(Email) + ", " + wsq(bool2tf(IsAdmin)) + ", " + wsq(bool2tf(IsSysadmin)) + ", " + wsq(Password) + ", " + wsq(Notes) + ", " + wsq(Stylesheet) + ")"
		assert DB.Exec(self.sql) == 1
		DB.Commit()
		return DB.Value('select max(user_id) from username')
	
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
		self.cursor = DB.Cursor()
		self.cursor.execute('SELECT user_id, username, session_id, first_name, middle_name, surname, email, admin, sysadmin, password, notes, stylesheet FROM username WHERE user_id=' + str(id))
		data = self.cursor.fetchone()
		self.ID		= data[0]
		self.Username	= trim(data[1])
		self.SessionID	= trim(data[2])
		self.FirstName	= trim(data[3])
		self.MiddleName	= trim(data[4])
		self.Surname	= trim(data[5])
		self.Email	= trim(data[6])
		self.IsAdmin	= tf2bool(data[7])
		self.IsSyadmin	= tf2bool(data[8])
		self.Password	= trim(data[9])
		self.Notes	= trim(data[10])
		self.Stylesheet	= trim(data[11])
		self.Name	= trim(trim(self.FirstName + ' ' + self.MiddleName) + ' ' + self.Surname)

		self.Docs = UserDocs(self.ID)


# Documents

class Docs(LampadasCollection):
	"""
	A collection object providing access to all documents.
	"""

	def __init__(self):
		self.cursor = DB.Cursor()
		self.cursor.execute("SELECT doc_id, title, class_id, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating, lang, sk_seriesid FROM document")
		while (1):
			data = self.cursor.fetchone()
			if data == None: break
			newDoc = Doc()
			newDoc.__load__(data)
			self.col[newDoc.ID] = newDoc

	def Add(self, Title, ClassID, Format, DTD, DTDVersion, Version, LastUpdate, URL, ISBN, PubStatus, ReviewStatus, TickleDate, PubDate, HomeURL, TechReviewStatus, License, Abstract, LanguageCode, SeriesID):
		self.id = DB.Value('select max(doc_id) from document') + 1
		self.sql = "INSERT INTO document(doc_id, title, class_id, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, license, abstract, lang, sk_seriesid) VALUES (" + str(self.id) + ", " + wsq(Title) + ", " + str(ClassID) + ", " + wsq(Format) + ", " + wsq(DTD) + ", " + wsq(DTDVersion) + ", " + wsq(Version) + ", " + wsq(LastUpdate) + ", " + wsq(URL) + ", " + wsq(ISBN) + ", " + wsq(PubStatus) + ", " + wsq(ReviewStatus) + ", " + wsq(TickleDate) + ", " + wsq(PubDate) + ", " + wsq(HomeURL) + ", " + wsq(TechReviewStatus) + ", " + wsq(License) + ", " + wsq(Abstract) + ", " + wsq(LanguageCode) + ", " + wsq(SeriesID) + ")"
		assert DB.Exec(self.sql) == 1
		DB.Commit()
		self.NewID = DB.Value('select max(doc_id) from document')
		newDoc = Doc(self.NewID)
		self.col[self.NewID] = newDoc
		return self.NewID
	
	def Del(self, id):
		self.sql = ('DELETE from document WHERE doc_id=' + str(id))
		assert DB.Exec(self.sql) == 1
		DB.Commit()
		del self.col[id]


class Doc:
	"""
	A document in any format, whether local or remote.
	"""

	def __init__(self, id=None):
		if id == None: return
		self.cursor = DB.Cursor()
		self.cursor.execute("SELECT doc_id, title, class_id, format, dtd, dtd_version, version, last_update, url, isbn, pub_status, review_status, tickle_date, pub_date, ref_url, tech_review_status, maintained, license, abstract, rating, lang, sk_seriesid FROM document WHERE doc_id=" + str(id))
		data = self.cursor.fetchone()
		self.__load__(data)

	def __load__(self, data):
		self.ID			= data[0]
		self.Title		= trim(data[1])
		self.ClassID		= data[2]
		self.Format		= trim(data[3])
		self.DTD		= trim(data[4])
		self.DTDVersion		= trim(data[5])
		self.Version		= trim(data[6])
		self.LastUpdate		= trim(data[7])
		self.URL		= trim(data[8])
		self.ISBN		= trim(data[9])
		self.PubStatus		= trim(data[10])
		self.ReviewStatus	= trim(data[11])
		self.TickleDate		= trim(data[12])
		self.PubDate		= trim(data[13])
		self.HomeURL		= trim(data[14])
		self.TechReviewStatus	= trim(data[15])
		self.Maintained		= tf2bool(data[16])
		self.License		= trim(data[17])
		self.Abstract		= trim(data[18])
		self.Rating		= data[19]
		self.LanguageCode	= trim(data[20])
		self.SeriesID		= trim(data[21])

	def Save(self):
		self.sql = "UPDATE document SET title=" + wsq(self.Title) + ", class_id=" + str(self.ClassID) + ", format=" + wsq(self.Format) + ", dtd=" + wsq(self.DTD) + ", dtd_version=" + wsq(self.DTDVersion) + ", version=" + wsq(self.Version) + ", last_update=" + wsq(self.LastUpdate) + ", url=" + wsq(self.URL) + ", isbn=" + wsq(self.ISBN) + ", pub_status=" + wsq(self.PubStatus) + ", review_status=" + wsq(self.ReviewStatus) + ", tickle_date=" + wsq(self.TickleDate) + ", pub_date=" + wsq(self.PubDate) + ", ref_url=" + wsq(self.HomeURL) + ", tech_review_status=" + wsq(self.TechReviewStatus) + ", maintained=" + wsq(bool2tf(self.Maintained)) + ", license=" + wsq(self.License) + ", abstract=" + wsq(self.Abstract) + ", rating=" + wsq(self.Rating) + ", lang=" + wsq(self.LanguageCode) + ", sk_seriesid=" + wsq(self.SeriesID) + " WHERE doc_id=" + str(self.ID)
		DB.Exec(self.sql)
		DB.Commit()


# UserDocs

class UserDocs(LampadasList):
	"""
	A collection object providing access to all user document associations.
	"""

	def __init__(self, UserID):
		assert not UserID == None
		self.UserID = UserID
		self.cursor = DB.Cursor()
		self.cursor.execute("SELECT doc_id, user_id, role, email, active FROM document_user WHERE user_id=" + str(self.UserID))
		while (1):
			row = self.cursor.fetchone()
			if row == None: break
			newUserDoc = UserDoc(UserID, row[0])
			newUserDoc.__load__(row)
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

	DocID	= None
	UserID	= None
	Role	= None
	Email	= None
	Active	= None

	def __init__(self, UserID=None, DocID=None):
		self.UserID = UserID
		self.DocID = DocID
		if DocID == None: return
		if UserID == None: return
		self.cursor = DB.Cursor()
		self.cursor.execute("SELECT doc_id, user_id, role, email, active FROM document_user WHERE doc_id=" + str(DocID) + " AND user_id=" + str(UserID))
		row = self.cursor.fetchone()
		self.__load__(row)

	def __load__(self, row):
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
	
