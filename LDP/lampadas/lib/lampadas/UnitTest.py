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

# Test Suite ###################################################################

#def TS():
#	TS = unittest.TestSuite()
#	TS.addTest(ConfigTest)
#	return TS


# Unit Tests ###################################################################

class testConfig(unittest.TestCase):

	def testConfig(self):
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


class testUsers(unittest.TestCase):

	def setUp(self):
		self.Users = DataLayer.Users()
		assert not self.Users == None
		assert self.Users.Count > 0

	def testUsers(self):
		DB.Exec("delete from username where email='foo@example.com'")
		DB.Commit()
	
		self.OldID = DB.Value('select max(user_id) from username')
		self.NewID = self.Users.Add('testuser', 'j', 'random', 'hacker', 'foo@example.com', 1, 1, 'pw', 'notes go here', 'default')
		assert self.NewID > 0
		assert self.OldID + 1 == self.NewID
		
		self.User = DataLayer.User(self.NewID)
		assert not self.User == None
		assert self.User.ID == self.NewID
		assert self.User.Username == 'testuser'
		assert self.User.Email == 'foo@example.com'
		
		self.Users.Del(self.NewID)
		self.NewID = DB.Value('select max(user_id) from username')
		assert self.NewID == self.OldID


class testUserDocs(unittest.TestCase):

	def setUp(self):
		self.User = User(1)
		assert self.User.Docs.Count > 0


class testDocs(unittest.TestCase):

	def setUp(self):
		self.Docs = DataLayer.Docs()
		assert not self.Docs == None
		assert self.Docs.Count > 0

	def testDocs(self):
		DB.Exec("delete from document where title='testharness'")
		DB.Commit()
	
		self.OldID = DB.Value('select max(doc_id) from document')
		self.NewID = self.Docs.Add('testharness', 1, 'XML', 'DocBook', '4.1.2', '1.0', '2002-04-04', 'http://www.example.com/HOWTO.html', 'ISBN', 'N', 'N', '2002-04-05', '2002-04-10', 'http://www.home.com', 'N', 'GFDL', 'This is a document.', 'EN', 'fooseries')
		assert self.NewID > 0
		assert self.OldID + 1 == self.NewID
		
		self.Doc = DataLayer.Doc(self.NewID)
		assert not self.Doc == None
		assert self.Doc.ID == self.NewID
		assert self.Doc.Title == 'testharness'
		
		self.Docs.Del(self.NewID)
		self.NewID = DB.Value('select max(doc_id) from document')
		assert self.NewID == self.OldID

	def testMapping(self):
		self.Doc = self.Docs[1]
		assert not self.Doc == None
		assert not self.Doc.Title == ''

	def testSave(self):
		self.Doc = self.Docs[1]
		self.Title = self.Doc.Title
		self.Doc.Title = 'Foo'
		assert self.Doc.Title == 'Foo'
		self.Doc.Save()
		self.Doc2 = DataLayer.Doc(1)
		assert self.Doc2.Title == 'Foo'
		
		self.Doc.Title = self.Title
		assert self.Doc.Title == self.Title
		self.Doc.Save()
		self.Doc2 = DataLayer.Doc(1)
		assert self.Doc2.Title == self.Title

if __name__ == "__main__":
	unittest.main()
