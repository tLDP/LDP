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
from URLParse import URI
from Log import log
import commands


# TESTS TO ADD:
# 
# make sure there are no conflicts between blocks and strings, which could
# confuse things.

# Unit Tests ###################################################################


class testConfigFile(unittest.TestCase):

    def testConfigFIle(self):
        log(3, 'testing Config file')
        assert config.db_type == "pgsql", "db_type is not valid"
        assert config.db_name == "lampadas", "Database name is not valid"
        assert config.cvs_root > ''
        log(3, 'testing config file done')


class testDatabase(unittest.TestCase):

    def setUp(self):
        db.connect(config.db_type, config.db_name)

    def testDatabase(self):
        log(3, 'testing database')
        assert not db.connection == None
        log(3, 'testing database done')

    def testCursor(self):
        log(3, 'testing cursor')
        cursor = db.cursor
        assert not cursor == None
        log(3, 'testing cursor done')


class testClasses(unittest.TestCase):

    def testClasses(self):
        log(3, 'testing classes')
        assert not lampadas.Classes == None
        assert lampadas.Classes.count() > 0
        log(3, 'testing classes done')


class testConfig(unittest.TestCase):

    def testConfig(self):
        log(3, 'testing Config')
        assert not config == None
        assert lampadas.Config['project_short'] == 'LDP'
        log(3, 'testing Config done')


class testDocs(unittest.TestCase):

    def testDocs(self):
        log(3, 'testing Docs')
        assert not lampadas.Docs == None
        assert lampadas.Docs.count() > 0

        db.runsql("DELETE FROM document where title='testharness'")
        db.commit()
    
        self.OldID = db.read_value('SELECT max(doc_id) from document')
        self.NewID = lampadas.Docs.add('testharness', 1, 1, 'DocBook', '4.1.2', '1.0', '2002-04-04', 'http://www.example.com/HOWTO.html', 'ISBN', 'N', 'N', '2002-04-05', '2002-04-10', 'http://www.home.com', 'N', 'GFDL', 'This is a document.', 'EN', 'fooseries')
        assert self.NewID > 0
        assert self.OldID + 1 == self.NewID
        
        self.Doc = lampadas.Doc(self.NewID)
        assert not self.Doc == None
        assert self.Doc.ID == self.NewID
        assert self.Doc.Title == 'testharness'
        assert self.Doc.FormatID == 1
        
        lampadas.Docs.Del(self.NewID)
        self.NewID = db.read_value('SELECT MAX(doc_id) from document')
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
            if Doc.Errs.count() > 0:
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
        assert Doc.Files.count() > 0
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
        assert Doc.Ratings.count() == 0
        assert Doc.Rating == 0

        # Add UserID: 1   Rating: 5   -- Avg: 5

        Doc.Ratings.add(1, 5)
        assert Doc.Ratings.count() == 1
        assert Doc.Ratings.Average == 5
        assert Doc.Rating == 5

        # Add UserID: 2   Rating: 7   -- Avg: 6
        
        Doc.Ratings.add(2, 7)
        assert Doc.Ratings.count() == 2
        assert Doc.Ratings.Average == 6
        assert Doc.Rating == 6

        # Del UserID: 1
    
        Doc.Ratings.Del(1)
        assert Doc.Ratings.count() == 1
        assert Doc.Ratings.Average == 7
        assert Doc.Rating == 7

        # Clear again

        Doc.Ratings.Clear()
        assert Doc.Ratings.count() == 0
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
            if Doc.Versions.count() > 0:
                found = 1
                vkeys = Doc.Versions.keys()
                for vkey in vkeys:
                    Version = Doc.Versions[vkey]
                    assert not Version == None
                    assert Version.PubDate > ''
                    assert Version.Initials > ''
        assert found == 1
        log(3, 'testing DocVersions done')


class testLicenses(unittest.TestCase):

    def testLicenses(self):
        log(3, 'testing Licenses')
        assert lampadas.Licenses.count() > 0
        assert not lampadas.Licenses['GPL'] == None
        log(3, 'testing Licenses done')


class testDTDs(unittest.TestCase):

    def testDTDs(self):
        log(3, 'testing DTDs')
        assert lampadas.DTDs.count() > 0
        assert not lampadas.DTDs['DocBook'] == None
        log(3, 'testing DTDs done')


class testFormats(unittest.TestCase):

    def testFormats(self):
        log(3, 'testing Formats')
        assert lampadas.Formats.count() > 0
        assert not lampadas.Formats[1] == None
        assert not lampadas.Formats[1].I18n == None
        assert not lampadas.Formats[1].I18n['EN'] == None
        assert lampadas.Formats[1].I18n['EN'].Name > ''
        assert lampadas.Formats[1].I18n['EN'].Description > ''
        log(3, 'testing Formats done')


class testLanguages(unittest.TestCase):

    def testLanguages(self):
        log(3, 'testing Languages')
        assert not lampadas.Languages == None
        assert not lampadas.Languages['EN'] == None
        assert lampadas.Languages['EN'].Supported
        assert lampadas.Languages['EN'].I18n['EN'].Name == 'English'
        assert lampadas.Languages['FR'].Supported
        assert lampadas.Languages['FR'].I18n['EN'].Name == 'French'
        assert lampadas.Languages.count() == 136
        log(3, 'testing Languages done')


class testPubStatuses(unittest.TestCase):

    def testPubStatuses(self):
        log(3, 'testing PubStatuses')
        assert not lampadas.PubStatuses == None
        assert lampadas.PubStatuses.count() > 0
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
        assert lampadas.Topics.count() > 0
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
        assert lampadas.Users.count() > 0

        db.runsql("DELETE FROM username where email='foo@example.com'")
        db.commit()
    
        self.OldID = db.read_value('SELECT MAX(user_id) from username')
        self.NewID = lampadas.Users.add('testuser', 'j', 'random', 'hacker', 'foo@example.com', 1, 1, 'pw', 'notes go here', 'default')
        assert self.NewID > 0
        assert self.OldID + 1 == self.NewID
        
        self.User = lampadas.User(self.NewID)
        assert not self.User == None
        assert self.User.ID == self.NewID
        assert self.User.Username == 'testuser'
        assert self.User.Email == 'foo@example.com'
        
        lampadas.Users.Del(self.NewID)
        self.NewID = db.read_value('SELECT MAX(user_id) from username')
        assert self.NewID == self.OldID
        log(3, 'testing Users done')


class testUserDocs(unittest.TestCase):

    def testUserDocs(self):
        log(3, 'testing UserDocs')
        self.User = lampadas.User(11)
        assert len(self.User.Docs) > 0
        assert self.User.Docs.count() > 0
        assert not self.User.Docs == None
        for UserDoc in self.User.Docs:
            assert not UserDoc == None
            assert not UserDoc.DocID == None
            assert UserDoc.DocID > 0
            assert UserDoc.Active == 1 or UserDoc.Active == 0
        log(3, 'testing UserDocs done')


class testUserDocs(unittest.TestCase):

    def testUserDocs(self):
        log(3, 'testing UserDocs')
        self.User = lampadas.User(11)
        assert len(self.User.Docs) > 0
        assert self.User.Docs.count() > 0
        assert not self.User.Docs == None
        for UserDoc in self.User.Docs:
            assert not UserDoc == None
            assert not UserDoc.DocID == None
            assert UserDoc.DocID > 0
            assert UserDoc.Active == 1 or UserDoc.Active == 0
            assert UserDoc.ID == UserDoc.DocID
        log(3, 'testing UserDocs done')


class testURLParse(unittest.TestCase):

    def check_uri(self, url, protocol, server, port, path, language, forcelang, id, format, filename, parameter, anchor):
        uri = URI(url)
        assert uri.protocol     == protocol
        assert uri.server       == server
        assert uri.port         == port
        assert uri.language     == language
        assert uri.force_lang   == forcelang
        assert uri.id           == id
        assert uri.format       == format
        assert uri.filename     == filename
        assert uri.parameter    == parameter
        assert uri.anchor       == anchor
        
    def testURLParse(self):
        #               uri                                     protocol    server          port    path    language    forcelang   id  format  filename    parameter   anchor
        self.check_uri('',                                      '',         '',             '',     '/',    'EN',       0,          0,  '',     'home',     '',         '')
        self.check_uri('/',                                     '',         '',             '',     '/',    'EN',       0,          0,  '',     'home',     '',         '')
        self.check_uri('/home',                                 '',         '',             '',     '/',    'EN',       0,          0,  '',     'home',     '',         '')
        self.check_uri('FR',                                    '',         '',             '',     '/',    'FR',       1,          0,  '',     'home',     '',         '')
        self.check_uri('FR/',                                   '',         '',             '',     '/',    'FR',       1,          0,  '',     'home',     '',         '')
        self.check_uri('FR/home',                               '',         '',             '',     '/',    'FR',       1,          0,  '',     'home',     '',         '')
        self.check_uri('/editdoc/1',                            '',         '',             '',     '/',    'EN',       0,          1,  '',     'editdoc',  '',         '')
        self.check_uri('ES/editdoc/1',                          '',         '',             '',     '/',    'ES',       1,          1,  '',     'editdoc',  '',         '')
        self.check_uri('http://localhost:8000',                 'http',     'localhost',    '8000', '/',    'EN',       0,          0,  '',     'home',     '',         '')
        self.check_uri('http://localhost/editdoc/1',            'http',     'localhost',    '',     '/',    'EN',       0,          1,  '',     'editdoc',  '',         '')
        self.check_uri('http://localhost/ES/editdoc/1',         'http',     'localhost',    '',     '/',    'ES',       1,          1,  '',     'editdoc',  '',         '')
        self.check_uri('http://localhost:8000/ES/editdoc/1',    'http',     'localhost',    '8000', '/',    'ES',       1,          1,  '',     'editdoc',  '',         '')
       

if __name__ == "__main__":
	unittest.main()
