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
Lampadas UnitTest Module
"""

import unittest
from Config import config
from Database import db
from DataLayer import lampadas
from Log import log
import commands

# Test Suite ###################################################################

#def TS():
#	TS = unittest.TestSuite()
#	TS.addTest(ConfigTest)
#	return TS


# Unit Tests ###################################################################


class testConfigFile(unittest.TestCase):

    def testConfigFIle(self):
        log(3, 'testing Config file')
        assert config.db_type == "pgsql", "DBType is not valid"
        assert config.db_name == "lampadas", "Database name is not valid"
        assert config.cvs_root > ''
        log(3, 'testing Config file done')


class testDatabase(unittest.TestCase):

    def setUp(self):
        DB.Connect(Config.DBType, Config.DBName)

    def testDatabase(self):
        log(3, 'testing database')
        assert not DB.Connection == None
        log(3, 'testing database done')

    def testCursor(self):
        log(3, 'testing cursor')
        self.Cursor = DB.Cursor
        assert not self.Cursor == None
        log(3, 'testing cursor done')


class testClasses(unittest.TestCase):

    def testClasses(self):
        log(3, 'testing classes')
        assert not L.Classes == None
        assert lampadas.Classes.Count() > 0
        log(3, 'testing classes done')


class testConfig(unittest.TestCase):

    def testConfig(self):
        log(3, 'testing Config')
        assert not config == None
        assert config['project_short'] == 'LDP'
        log(3, 'testing Config done')


class testDocs(unittest.TestCase):

    def testDocs(self):
        log(3, 'testing Docs')
        assert not lampadas.Docs == None
        assert lampadas.Docs.Count() > 0

        DB.Exec("DELETE FROM document where title='testharness'")
        DB.Commit()
    
        self.OldID = DB.Value('SELECT max(doc_id) from document')
        self.NewID = lampadas.Docs.Add('testharness', 1, 1, 'DocBook', '4.1.2', '1.0', '2002-04-04', 'http://www.example.com/HOWTO.html', 'ISBN', 'N', 'N', '2002-04-05', '2002-04-10', 'http://www.home.com', 'N', 'GFDL', 'This is a document.', 'EN', 'fooseries')
        assert self.NewID > 0
        assert self.OldID + 1 == self.NewID
        
        self.Doc = lampadas.Doc(self.NewID)
        assert not self.Doc == None
        assert self.Doc.ID == self.NewID
        assert self.Doc.Title == 'testharness'
        assert self.Doc.FormatID == 1
        
        lampadas.Docs.Del(self.NewID)
        self.NewID = DB.Value('SELECT MAX(doc_id) from document')
        assert self.NewID == self.OldID

        keys = lampadas.Docs.keys()
        for key in keys:
            self.Doc = lampadas.Docs[key]
            assert self.Doc.ID == key
        log(3, 'testing Docs done')

    def testMapping(self):
        log(3, 'testing Docs Mapping')
        self.Doc = lampadas.Docs[100]
        assert not self.Doc == None
        assert not self.Doc.Title == ''
        assert self.Doc.ID == 100
        self.Doc = lampadas.Docs[2]
        assert self.Doc.ID == 2
        log(3, 'testing Docs Mapping done')

    def testSave(self):
        log(3, 'testing Docs Save')
        self.Doc = lampadas.Docs[100]
        self.Title = self.Doc.Title
        self.Doc.Title = 'Foo'
        assert self.Doc.Title == 'Foo'
        self.Doc.Save()
        self.Doc2 = lampadas.Docs[100]
        assert self.Doc2.Title == 'Foo'
        
        self.Doc.Title = self.Title
        assert self.Doc.Title == self.Title
        self.Doc.Save()
        self.Doc2 = lampadas.Docs[100]
        assert self.Doc2.Title == self.Title
        log(3, 'testing Docs Save done')


class testDocErrs(unittest.TestCase):

    def testDocErrs(self):
        log(3, 'testing DocErrs')
        keys = lampadas.Docs.keys()
        for key in keys:
            Doc = lampadas.Docs[key]
            assert not Doc == None
            if Doc.Errs.Count() > 0:
                log("found a doc with errors")
                for Err in Doc.Errs:
                    assert not Err == None
                    assert Err.DocID == Doc.ID
                    assert Err.ErrID > 1
        log(3, 'testing DocErrs done')
    

class testDocFiles(unittest.TestCase):

    def testDocFiles(self):
        log(3, 'testing DocFiles')
        Doc = lampadas.Docs[100]
        assert not Doc == None
        assert Doc.Files.Count() > 0
        keys = Doc.Files.keys()
        for key in keys:
            File = Doc.Files[key]
            if File == None: break
            assert File.DocID == Doc.ID
            assert File.Filename > ''
        log(3, 'testing DocFiles done')


class testDocRatings(unittest.TestCase):

    def testDocRatings(self):
        log(3, 'testing DocRatings')
        Doc = lampadas.Docs[100]
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
        log(3, 'testing DocRatings done')


class testDocVersions(unittest.TestCase):

    def testDocVersions(self):
        log(3, 'testing DocVersions')
        keys = lampadas.Docs.keys()
        found = 0
        for key in keys:
            Doc = lampadas.Docs[key]
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
        log(3, 'testing DocVersions done')


class testDTDs(unittest.TestCase):

    def testDTDs(self):
        log(3, 'testing DTDs')
        assert lampadas.DTDs.Count() > 0
        assert not lampadas.DTDs['DocBook'] == None
        log(3, 'testing DTDs done')


class testFormats(unittest.TestCase):

    def testFormats(self):
        log(3, 'testing Formats')
        assert lampadas.Formats.Count() > 0
        assert not lampadas.Formats[1] == None
        assert not lampadas.Formats[1].I18n == None
        assert not lampadas.Formats[1].I18n['EN'] == None
        assert lampadas.Formats[1].I18n['EN'].Name > ''
        assert lampadas.Formats[1].I18n['EN'].Description > ''
        log(3, 'testing Formats done')


class testLanguages(unittest.TestCase):

    def testLanguages(self):
        log(3, 'testing Languages')
        assert lampadas.Languages['EN'].Supported
        assert lampadas.Languages['EN'].I18n['EN'].Name == 'English'
        assert lampadas.Languages['FR'].Supported
        assert lampadas.Languages['FR'].I18n['EN'].Name == 'French'
        assert lampadas.Languages.Count() == 136
        log(3, 'testing Languages done')


class testPubStatuses(unittest.TestCase):

    def testPubStatuses(self):
        log(3, 'testing PubStatuses')
        assert not lampadas.PubStatuses == None
        assert lampadas.PubStatuses.Count() > 0
        assert not lampadas.PubStatuses['A'] == None
        assert not lampadas.PubStatuses['A'].I18n == None
        assert not lampadas.PubStatuses['A'].I18n['EN'] == None
        assert lampadas.PubStatuses['A'].I18n['EN'].Name > ''
        assert lampadas.PubStatuses['A'].I18n['EN'].Description > ''
        log(3, 'testing PubStatuses done')
        

class testTopics(unittest.TestCase):

    def testTopics(self):
        log(3, 'testing Topics')
        assert not lampadas.Topics == None
        assert lampadas.Topics.Count() > 0
        keys = lampadas.Topics.keys()
        for key in keys:
            Topic = lampadas.Topics[key]
            assert Topic.Num > 0
            assert Topic.I18n['EN'].Name > ''
        log(3, 'testing Topics done')


class testUsers(unittest.TestCase):

    def testUsers(self):
        log(3, 'testing Users')
        assert not lampadas.Users == None
        assert lampadas.Users.Count() > 0

        DB.Exec("DELETE FROM username where email='foo@example.com'")
        DB.Commit()
    
        self.OldID = DB.Value('SELECT MAX(user_id) from username')
        self.NewID = lampadas.Users.Add('testuser', 'j', 'random', 'hacker', 'foo@example.com', 1, 1, 'pw', 'notes go here', 'default')
        assert self.NewID > 0
        assert self.OldID + 1 == self.NewID
        
        self.User = lampadas.User(self.NewID)
        assert not self.User == None
        assert self.User.ID == self.NewID
        assert self.User.Username == 'testuser'
        assert self.User.Email == 'foo@example.com'
        
        lampadas.Users.Del(self.NewID)
        self.NewID = DB.Value('SELECT MAX(user_id) from username')
        assert self.NewID == self.OldID
        log(3, 'testing Users done')


class testUserDocs(unittest.TestCase):

    def testUserDocs(self):
        log(3, 'testing UserDocs')
        self.User = lampadas.User(11)
        assert len(self.User.Docs) > 0
        assert self.User.Docs.Count() > 0
        assert not self.User.Docs == None
        for UserDoc in self.User.Docs:
            assert not UserDoc == None
            assert not UserDoc.DocID == None
            assert UserDoc.DocID > 0
            assert UserDoc.DocID == UserDoc.ID
            assert UserDoc.Active == 1 or UserDoc.Active == 0
        log(3, 'testing UserDocs done')


#class testConverter(unittest.TestCase):
#
#	import Converter
#
#	def setUp(self):
#		self.C = Converter.Converter()
#
#	def run(self, dir, base, ext, output):
#		self.filename	= dir + base + ext
#		self.xmlnew		= dir + base + '.xml.new'
#		self.md5new		= dir + base + '.md5.new'
#		self.md5old		= dir + base + '.md5.old'
#	
#		fd = open(self.xmlnew, 'w')
#		fd.write(output + "\n")
#		fd.close()
#
#		newchecksum = commands.getoutput('md5sum < ' + self.xmlnew)
#		newchecksum = newchecksum + "\n"
#		
#		fd = open(self.md5new, 'w')
#		fd.write(newchecksum)
#		fd.close()
#
#		fd = open(self.md5old, 'r')
#		oldchecksum = fd.read()
#		fd.close()
#
#		assert oldchecksum == newchecksum
#
#	def testWikiText(self):
#		
#		output = self.C.wikitext('test/wt/Lampadas.wt')
#		self.run('test/wt/', 'Lampadas', '.wt', output)
#
#	def testTexinfo(self):
#		output = self.C.texinfo('test/texinfo/texinfo.txi')
#		self.run('test/texinfo/', 'texinfo', '.txi', output)
#
#	def testDBSGML(self):
#		output = self.C.dbsgml('test/db3.0sgml/RPM-HOWTO.sgml')
#		self.run('test/db3.0sgml/', 'RPM-HOWTO', '.sgml', output)
#		
#		output = self.C.dbsgml('test/db3.1sgml/XFree86-Second-Mouse.sgml')
#		self.run('test/db3.1sgml/', 'XFree86-Second-Mouse', '.sgml', output)
#
#		output = self.C.dbsgml('test/db4.1sgml/Small-Memory.sgml')
#		self.run('test/db4.1sgml/', 'Small-Memory', '.sgml', output)

#class testHTML(unittest.TestCase):
    
#	def setUp(self):
#		self.HTML = HTMlampadas.HTMLFactory()

#	def testHTML(self):
#		assert not self.HTMlampadas.Page == None
#		assert self.HTMlampadas.Page('test', 'EN') > ''


if __name__ == "__main__":
    unittest.main()
