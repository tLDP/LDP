#!/usr/bin/python

"""
Lampadas UnitTest Module
"""

import unittest
import Config
import Database
import DataLayer

Config = Config.Config()
DB = Database.Database()

L = DataLayer.Lampadas()

# Test Suite ###################################################################

#def TS():
#	TS = unittest.TestSuite()
#	TS.addTest(ConfigTest)
#	return TS


# Unit Tests ###################################################################

class testConfigFIle(unittest.TestCase):

	def testConfigFIle(self):
		assert Config.DBType == "pgsql", "DBType is not valid"
		assert Config.DBName == "lampadas", "Database name is not valid"


class testDatabase(unittest.TestCase):

	def setUp(self):
		DB.Connect(Config.DBType, Config.DBName)

	def testDatabase(self):
		assert not DB.Connection == None

	def testCursor(self):
		self.Cursor = DB.Cursor
		assert not self.Cursor == None


class testClasses(unittest.TestCase):

	def testClasses(self):
		assert not L.Classes == None
		assert L.Classes.Count() > 0


class testConfig(unittest.TestCase):

	def testConfig(self):
		assert not L.Config == None
		assert not L.Config['cvs_root'] == None
		assert L.Config['project_short'] == 'LDP'

class testDocs(unittest.TestCase):

	def testDocs(self):
		assert not L.Docs == None
		assert L.Docs.Count() > 0

		DB.Exec("DELETE FROM document where title='testharness'")
		DB.Commit()
	
		self.OldID = DB.Value('SELECT max(doc_id) from document')
		self.NewID = L.Docs.Add('testharness', 1, 'XML', 'DocBook', '4.1.2', '1.0', '2002-04-04', 'http://www.example.com/HOWTO.html', 'ISBN', 'N', 'N', '2002-04-05', '2002-04-10', 'http://www.home.com', 'N', 'GFDL', 'This is a document.', 'EN', 'fooseries')
		assert self.NewID > 0
		assert self.OldID + 1 == self.NewID
		
		self.Doc = L.Doc(self.NewID)
		assert not self.Doc == None
		assert self.Doc.ID == self.NewID
		assert self.Doc.Title == 'testharness'
		
		L.Docs.Del(self.NewID)
		self.NewID = DB.Value('SELECT MAX(doc_id) from document')
		assert self.NewID == self.OldID

		keys = L.Docs.keys()
		for key in keys:
			self.Doc = L.Docs[key]
			assert self.Doc.ID == key

	def testMapping(self):
		self.Doc = L.Docs[1]
		assert not self.Doc == None
		assert not self.Doc.Title == ''
		assert self.Doc.ID == 1
		self.Doc = L.Docs[2]
		assert self.Doc.ID == 2

	def testSave(self):
		self.Doc = L.Docs[1]
		self.Title = self.Doc.Title
		self.Doc.Title = 'Foo'
		assert self.Doc.Title == 'Foo'
		self.Doc.Save()
		self.Doc2 = L.Docs[1]
		assert self.Doc2.Title == 'Foo'
		
		self.Doc.Title = self.Title
		assert self.Doc.Title == self.Title
		self.Doc.Save()
		self.Doc2 = L.Docs[1]
		assert self.Doc2.Title == self.Title

class testStrings(unittest.TestCase):

	def testStrings(self):
		assert not L.Strings == None
		assert L.Strings.Count() > 0
		assert not L.Strings['header'] == None
		assert L.Strings['test'].I18n['EN'].Text == 'Test Text'
		
class testUsers(unittest.TestCase):

	def testUsers(self):
		assert not L.Users == None
		assert L.Users.Count() > 0

		DB.Exec("DELETE FROM username where email='foo@example.com'")
		DB.Commit()
	
		self.OldID = DB.Value('SELECT MAX(user_id) from username')
		self.NewID = L.Users.Add('testuser', 'j', 'random', 'hacker', 'foo@example.com', 1, 1, 'pw', 'notes go here', 'default')
		assert self.NewID > 0
		assert self.OldID + 1 == self.NewID
		
		self.User = L.User(self.NewID)
		assert not self.User == None
		assert self.User.ID == self.NewID
		assert self.User.Username == 'testuser'
		assert self.User.Email == 'foo@example.com'
		
		L.Users.Del(self.NewID)
		self.NewID = DB.Value('SELECT MAX(user_id) from username')
		assert self.NewID == self.OldID


class testUserDocs(unittest.TestCase):

	def setUp(self):
		self.User = L.User(1)
		assert len(self.User.Docs) > 0
		assert self.User.Docs.Count() > 0

	def testUserDocs(self):
		assert not self.User.Docs == None
		for UserDoc in self.User.Docs:
			assert not UserDoc == None
			assert not UserDoc.DocID == None
			assert UserDoc.DocID > 0
			assert UserDoc.Active == 1 or UserDoc.Active == 0



if __name__ == "__main__":
	unittest.main()
