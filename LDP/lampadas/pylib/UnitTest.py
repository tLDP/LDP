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

class testDocErrors(unittest.TestCase):

	def testDocErrors(self):
		keys = L.Docs.keys()
		for key in keys:
			Doc = L.Docs[key]
			assert not Doc == None
			if Doc.Errors.Count() > 0:
				print "found a doc with errors"
				for Error in Doc.Errors:
					assert not Error == None
					assert Error.DocID == Doc.ID
					assert Error.Error > ''
	
class testDocFiles(unittest.TestCase):

	def testDocFiles(self):
		Doc = L.Docs[1]
		assert not Doc == None
		assert Doc.Files.Count() > 0
		keys = Doc.Files.keys()
		for key in keys:
			File = Doc.Files[key]
			if File == None: break
			assert File.DocID == Doc.ID
			assert File.Filename > ''

class testDocRatings(unittest.TestCase):

	def testDocRatings(self):
		Doc = L.Docs[1]
		assert not Doc == None
		Doc.Ratings.Clear()
		assert Doc.Ratings.Count() == 0
		assert Doc.Rating == 0

		# Add UserID: 1   Rating: 5   -- Avg: 5

		Doc.Ratings.Add(1, 5)
		assert Doc.Ratings.Count() == 1
		assert Doc.Ratings.Average == 5
		assert Doc.Rating == 5

		# Add UserID: 2   Rating: 7   -- Avg: 6
		
		Doc.Ratings.Add(2, 7)
		assert Doc.Ratings.Count() == 2
		assert Doc.Ratings.Average == 6
		assert Doc.Rating == 6

		# Del UserID: 1
	
		Doc.Ratings.Del(1)
		assert Doc.Ratings.Count() == 1
		assert Doc.Ratings.Average == 7
		assert Doc.Rating == 7

		# Clear again

		Doc.Ratings.Clear()
		assert Doc.Ratings.Count() == 0
		assert Doc.Ratings.Average == 0
		assert Doc.Rating == 0

class testDocVersions(unittest.TestCase):

	def testDocVersions(self):
		keys = L.Docs.keys()
		found = 0
		for key in keys:
			Doc = L.Docs[key]
			assert not Doc == None
			if Doc.Versions.Count() > 0:
				found = 1
				vkeys = Doc.Versions.keys()
				for vkey in vkeys:
					Version = Doc.Versions[vkey]
					assert not Version == None
					assert Version.PubDate > ''
					assert Version.Initials > ''
		assert found == 1

class testDTDs(unittest.TestCase):

	def testDTDs(self):
		assert L.DTDs.Count() > 0
		assert not L.DTDs['DocBook'] == None

class testFormats(unittest.TestCase):

	def testFormats(self):
		assert L.Formats.Count() > 0
		assert not L.Formats['XML'] == None

class testLanguages(unittest.TestCase):

	def testLanguages(self):
		assert L.Languages['EN'].Name == 'English'
		assert L.Languages['FR'].Name == 'French'
		assert L.Languages.Count() == 136

class testStrings(unittest.TestCase):

	def testStrings(self):
		assert not L.Strings == None
		assert L.Strings.Count() > 0
		assert not L.Strings['header'] == None
		assert L.Strings['test'].I18n['EN'].Text == 'Test Text'

class testTopics(unittest.TestCase):

	def testTopics(self):
		assert not L.Topics == None
		assert L.Topics.Count() > 0
		keys = L.Topics.keys()
		for key in keys:
			Topic = L.Topics[key]
			assert Topic.Num > 0
			assert Topic.I18n['EN'].Name > ''

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
