#!/usr/bin/python

"""
Lampadas UnitTest Module
"""

import unittest
import Config
import Database
import DataLayer
import Converter
#import HTML
import commands

Config = Config.Config()
DB = Database.Database()

L = DataLayer.Lampadas()

# Test Suite ###################################################################

#def TS():
#	TS = unittest.TestSuite()
#	TS.addTest(ConfigTest)
#	return TS


# Unit Tests ###################################################################

class testConfigFile(unittest.TestCase):

	def testConfigFIle(self):
		L.Log(3, 'testing Config file')
		assert Config.DBType == "pgsql", "DBType is not valid"
		assert Config.DBName == "lampadas", "Database name is not valid"
		assert Config.CVSRoot > ''
		L.Log(3, 'testing Config file done')

class testDatabase(unittest.TestCase):

	def setUp(self):
		DB.Connect(Config.DBType, Config.DBName)

	def testDatabase(self):
		L.Log(3, 'testing database')
		assert not DB.Connection == None
		L.Log(3, 'testing database done')

	def testCursor(self):
		L.Log(3, 'testing cursor')
		self.Cursor = DB.Cursor
		assert not self.Cursor == None
		L.Log(3, 'testing cursor done')

class testClasses(unittest.TestCase):

	def testClasses(self):
		L.Log(3, 'testing classes')
		assert not L.Classes == None
		assert L.Classes.Count() > 0
		L.Log(3, 'testing classes done')

class testConfig(unittest.TestCase):

	def testConfig(self):
		L.Log(3, 'testing Config')
		assert not L.Config == None
		assert L.Config['project_short'] == 'LDP'
		L.Log(3, 'testing Config done')

class testDocs(unittest.TestCase):

	def testDocs(self):
		L.Log(3, 'testing Docs')
		assert not L.Docs == None
		assert L.Docs.Count() > 0

		DB.Exec("DELETE FROM document where title='testharness'")
		DB.Commit()
	
		self.OldID = DB.Value('SELECT max(doc_id) from document')
		self.NewID = L.Docs.Add('testharness', 1, 1, 'DocBook', '4.1.2', '1.0', '2002-04-04', 'http://www.example.com/HOWTO.html', 'ISBN', 'N', 'N', '2002-04-05', '2002-04-10', 'http://www.home.com', 'N', 'GFDL', 'This is a document.', 'EN', 'fooseries')
		assert self.NewID > 0
		assert self.OldID + 1 == self.NewID
		
		self.Doc = L.Doc(self.NewID)
		assert not self.Doc == None
		assert self.Doc.ID == self.NewID
		assert self.Doc.Title == 'testharness'
		assert self.Doc.FormatID == 1
		
		L.Docs.Del(self.NewID)
		self.NewID = DB.Value('SELECT MAX(doc_id) from document')
		assert self.NewID == self.OldID

		keys = L.Docs.keys()
		for key in keys:
			self.Doc = L.Docs[key]
			assert self.Doc.ID == key
		L.Log(3, 'testing Docs done')

	def testMapping(self):
		L.Log(3, 'testing Docs Mapping')
		self.Doc = L.Docs[100]
		assert not self.Doc == None
		assert not self.Doc.Title == ''
		assert self.Doc.ID == 100
		self.Doc = L.Docs[2]
		assert self.Doc.ID == 2
		L.Log(3, 'testing Docs Mapping done')

	def testSave(self):
		L.Log(3, 'testing Docs Save')
		self.Doc = L.Docs[100]
		self.Title = self.Doc.Title
		self.Doc.Title = 'Foo'
		assert self.Doc.Title == 'Foo'
		self.Doc.Save()
		self.Doc2 = L.Docs[100]
		assert self.Doc2.Title == 'Foo'
		
		self.Doc.Title = self.Title
		assert self.Doc.Title == self.Title
		self.Doc.Save()
		self.Doc2 = L.Docs[100]
		assert self.Doc2.Title == self.Title
		L.Log(3, 'testing Docs Save done')

class testDocErrs(unittest.TestCase):

	def testDocErrs(self):
		L.Log(3, 'testing DocErrs')
		keys = L.Docs.keys()
		for key in keys:
			Doc = L.Docs[key]
			assert not Doc == None
			if Doc.Errs.Count() > 0:
				print "found a doc with errors"
				for Err in Doc.Errs:
					assert not Err == None
					assert Err.DocID == Doc.ID
					assert Err.ErrID > 1
		L.Log(3, 'testing DocErrs done')
	
class testDocFiles(unittest.TestCase):

	def testDocFiles(self):
		L.Log(3, 'testing DocFiles')
		Doc = L.Docs[100]
		assert not Doc == None
		assert Doc.Files.Count() > 0
		keys = Doc.Files.keys()
		for key in keys:
			File = Doc.Files[key]
			if File == None: break
			assert File.DocID == Doc.ID
			assert File.Filename > ''
		L.Log(3, 'testing DocFiles done')

class testDocRatings(unittest.TestCase):

	def testDocRatings(self):
		L.Log(3, 'testing DocRatings')
		Doc = L.Docs[100]
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
		L.Log(3, 'testing DocRatings done')

class testDocVersions(unittest.TestCase):

	def testDocVersions(self):
		L.Log(3, 'testing DocVersions')
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
		L.Log(3, 'testing DocVersions done')

class testDTDs(unittest.TestCase):

	def testDTDs(self):
		L.Log(3, 'testing DTDs')
		assert L.DTDs.Count() > 0
		assert not L.DTDs['DocBook'] == None
		L.Log(3, 'testing DTDs done')

class testFormats(unittest.TestCase):

	def testFormats(self):
		L.Log(3, 'testing Formats')
		assert L.Formats.Count() > 0
		assert not L.Formats[1] == None
		assert not L.Formats[1].I18n == None
		assert not L.Formats[1].I18n['EN'] == None
		assert L.Formats[1].I18n['EN'].Name > ''
		assert L.Formats[1].I18n['EN'].Description > ''
		L.Log(3, 'testing Formats done')

class testLanguages(unittest.TestCase):

	def testLanguages(self):
		L.Log(3, 'testing Languages')
		assert L.Languages['EN'].Supported
		assert L.Languages['EN'].I18n['EN'].Name == 'English'
		assert L.Languages['FR'].Supported
		assert L.Languages['FR'].I18n['EN'].Name == 'French'
		assert L.Languages.Count() == 136
		L.Log(3, 'testing Languages done')

class testPubStatuses(unittest.TestCase):

	def testPubStatuses(self):
		L.Log(3, 'testing PubStatuses')
		assert not L.PubStatuses == None
		assert L.PubStatuses.Count() > 0
		assert not L.PubStatuses['A'] == None
		assert not L.PubStatuses['A'].I18n == None
		assert not L.PubStatuses['A'].I18n['EN'] == None
		assert L.PubStatuses['A'].I18n['EN'].Name > ''
		assert L.PubStatuses['A'].I18n['EN'].Description > ''
		L.Log(3, 'testing PubStatuses done')
		
class testTopics(unittest.TestCase):

	def testTopics(self):
		L.Log(3, 'testing Topics')
		assert not L.Topics == None
		assert L.Topics.Count() > 0
		keys = L.Topics.keys()
		for key in keys:
			Topic = L.Topics[key]
			assert Topic.Num > 0
			assert Topic.I18n['EN'].Name > ''
		L.Log(3, 'testing Topics done')

class testUsers(unittest.TestCase):

	def testUsers(self):
		L.Log(3, 'testing Users')
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
		L.Log(3, 'testing Users done')

class testUserDocs(unittest.TestCase):


	def testUserDocs(self):
		L.Log(3, 'testing UserDocs')
		self.User = L.User(11)
		assert len(self.User.Docs) > 0
		assert self.User.Docs.Count() > 0
		assert not self.User.Docs == None
		for UserDoc in self.User.Docs:
			assert not UserDoc == None
			assert not UserDoc.DocID == None
			assert UserDoc.DocID > 0
			assert UserDoc.Active == 1 or UserDoc.Active == 0
		L.Log(3, 'testing UserDocs done')

class testConverter(unittest.TestCase):

	def setUp(self):
		self.C = Converter.Converter()

	def run(self, dir, base, ext, output):
		self.filename	= dir + base + ext
		self.xmlnew		= dir + base + '.xml.new'
		self.md5new		= dir + base + '.md5.new'
		self.md5old		= dir + base + '.md5.old'
	
		fd = open(self.xmlnew, 'w')
		fd.write(output + "\n")
		fd.close()

		newchecksum = commands.getoutput('md5sum < ' + self.xmlnew)
		newchecksum = newchecksum + "\n"
		
		fd = open(self.md5new, 'w')
		fd.write(newchecksum)
		fd.close()

		fd = open(self.md5old, 'r')
		oldchecksum = fd.read()
		fd.close()

		assert oldchecksum == newchecksum

	def testWikiText(self):
		
		output = self.C.wikitext('test/wt/Lampadas.wt')
		self.run('test/wt/', 'Lampadas', '.wt', output)

	def testTexinfo(self):
		output = self.C.texinfo('test/texinfo/texinfo.txi')
		self.run('test/texinfo/', 'texinfo', '.txi', output)

	def testDBSGML(self):
		output = self.C.dbsgml('test/db3.0sgml/RPM-HOWTO.sgml')
		self.run('test/db3.0sgml/', 'RPM-HOWTO', '.sgml', output)
		
		output = self.C.dbsgml('test/db3.1sgml/XFree86-Second-Mouse.sgml')
		self.run('test/db3.1sgml/', 'XFree86-Second-Mouse', '.sgml', output)

		output = self.C.dbsgml('test/db4.1sgml/Small-Memory.sgml')
		self.run('test/db4.1sgml/', 'Small-Memory', '.sgml', output)

#class testHTML(unittest.TestCase):
	
#	def setUp(self):
#		self.HTML = HTML.HTMLFactory()

#	def testHTML(self):
#		assert not self.HTML.Page == None
#		assert self.HTML.Page('test', 'EN') > ''


if __name__ == "__main__":
	unittest.main()
