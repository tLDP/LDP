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
        assert config.db_type=="pgsql"
        assert config.db_name > ''
        assert config.cvs_root > ''
        log(3, 'testing config file done')


class testDatabase(unittest.TestCase):

    def setUp(self):
        db.connect(config.db_type, config.db_name)

    def testDatabase(self):
        log(3, 'testing database')
        assert not db.connection==None
        log(3, 'testing database done')

    def testCursor(self):
        log(3, 'testing cursor')
        cursor = db.cursor
        assert not cursor==None
        log(3, 'testing cursor done')


class testClasses(unittest.TestCase):

    def testClasses(self):
        log(3, 'testing classes')
        assert not lampadas.Classes==None
        assert lampadas.Classes.count() > 0
        log(3, 'testing classes done')


class testConfig(unittest.TestCase):

    def testConfig(self):
        log(3, 'testing Config')
        assert not config==None
        assert lampadas.Config['project_short']=='LDP'
        log(3, 'testing Config done')


class testDocs(unittest.TestCase):

    def testDocs(self):
        log(3, 'testing Docs')
        assert not lampadas.docs==None
        assert lampadas.docs.count() > 0

        db.runsql("DELETE FROM document where title='testharness'")
        db.commit()
    
        self.Oldid = db.read_value('SELECT max(doc_id) from document')
        self.Newid = lampadas.docs.add('testharness', 1, 1, 'DocBook', '4.1.2', '1.0', '2002-04-04', 'http://www.example.com/HOWTO.html', 'ISBN', 'N', 'N', '2002-04-05', '2002-04-10', 'http://www.home.com', 'N', 'GFDL', 'This is a document.', 'EN', 'fooseries')
        assert self.Newid > 0
        assert self.Oldid + 1==self.Newid
        
        self.Doc = lampadas.docs[self.Newid]
        assert not self.Doc==None
        assert self.Doc.id==self.Newid
        assert self.Doc.title=='testharness'
        assert self.Doc.Formatid==1
        
        lampadas.docs.Del(self.Newid)
        self.Newid = db.read_value('SELECT MAX(doc_id) from document')
        assert self.Newid==self.Oldid

        keys = lampadas.docs.keys()
        for key in keys:
            self.Doc = lampadas.docs[key]
            assert self.Doc.id==key
        log(3, 'testing Docs done')

    def testMapping(self):
        log(3, 'testing Docs Mapping')
        self.Doc = lampadas.docs[100]
        assert not self.Doc==None
        assert not self.Doc.title==''
        assert self.Doc.id==100
        self.Doc = lampadas.docs[2]
        assert self.Doc.id==2
        log(3, 'testing Docs Mapping done')

    def test_save(self):
        log(3, 'testing doc.save()')
        self.Doc = lampadas.docs[100]
        self.title = self.Doc.title
        self.Doc.title = 'Foo'
        assert self.Doc.title=='Foo'
        self.Doc.save()
        self.Doc2 = lampadas.docs[100]
        assert self.Doc2.title=='Foo'
        
        self.Doc.title = self.title
        assert self.Doc.title==self.title
        self.Doc.save()
        self.Doc2 = lampadas.docs[100]
        assert self.Doc2.title==self.title
        log(3, 'testing doc.save done')


class testDocErrs(unittest.TestCase):

    def testDocErrs(self):
        log(3, 'testing DocErrs')
        keys = lampadas.docs.keys()
        for key in keys:
            Doc = lampadas.docs[key]
            assert not Doc==None
            if Doc.Errs.count() > 0:
                log("found a doc with errors")
                for Err in Doc.Errs:
                    assert not Err==None
                    assert Err.doc_id==Doc.id
                    assert Err.Errid > 1
        log(3, 'testing DocErrs done')
    

class testDocFiles(unittest.TestCase):

    def testDocFiles(self):
        log(3, 'testing DocFiles')
        Doc = lampadas.docs[100]
        assert not Doc==None
        assert Doc.files.count() > 0
        keys = Doc.files.keys()
        for key in keys:
            File = Doc.files[key]
            if File==None: break
            assert File.doc_id==Doc.id
            assert File.filename > ''
        log(3, 'testing DocFiles done')


class testDocRatings(unittest.TestCase):

    def testDocRatings(self):
        log(3, 'testing DocRatings')
        Doc = lampadas.docs[100]
        assert not Doc==None
        Doc.Ratings.clear()
        assert Doc.Ratings.count()==0
        assert Doc.Rating==0

        # Add Userid: 1   Rating: 5   -- Avg: 5

        Doc.Ratings.add(1, 5)
        assert Doc.Ratings.count()==1
        assert Doc.Ratings.Average==5
        assert Doc.Rating==5

        # Add Userid: 2   Rating: 7   -- Avg: 6
        
        Doc.Ratings.add(2, 7)
        assert Doc.Ratings.count()==2
        assert Doc.Ratings.Average==6
        assert Doc.Rating==6

        # Del Userid: 1
    
        Doc.Ratings.Del(1)
        assert Doc.Ratings.count()==1
        assert Doc.Ratings.Average==7
        assert Doc.Rating==7

        # Clear again

        Doc.Ratings.clear()
        assert Doc.Ratings.count()==0
        assert Doc.Ratings.Average==0
        assert Doc.Rating==0
        log(3, 'testing DocRatings done')


class testDocVersions(unittest.TestCase):

    def testDocVersions(self):
        log(3, 'testing DocVersions')
        keys = lampadas.docs.keys()
        found = 0
        for key in keys:
            Doc = lampadas.docs[key]
            assert not Doc==None
            if Doc.versions.count() > 0:
                found = 1
                vkeys = Doc.versions.keys()
                for vkey in vkeys:
                    version = Doc.versions[vkey]
                    assert not version==None
                    assert version.PubDate > ''
                    assert version.Initials > ''
        assert found==1
        log(3, 'testing DocVersions done')


class testLicenses(unittest.TestCase):

    def testLicenses(self):
        log(3, 'testing Licenses')
        assert lampadas.Licenses.count() > 0
        assert not lampadas.Licenses['GPL']==None
        log(3, 'testing Licenses done')


class test_dtds(unittest.TestCase):

    def test_dtdss(self):
        log(3, 'testing DTDs')
        assert lampadas.dtds.count() > 0
        assert not lampadas.dtds['DocBook']==None
        log(3, 'testing DTDs done')


class testFormats(unittest.TestCase):

    def testFormats(self):
        log(3, 'testing Formats')
        assert lampadas.formats.count() > 0
        assert not lampadas.formats[1]==None
        assert not lampadas.formats[1].I18n==None
        assert not lampadas.formats[1].I18n['EN']==None
        assert lampadas.formats[1].I18n['EN'].Name > ''
        assert lampadas.formats[1].I18n['EN'].Description > ''
        log(3, 'testing Formats done')


class testLanguages(unittest.TestCase):

    def testLanguages(self):
        log(3, 'testing Languages')
        assert not lampadas.languages==None
        assert not lampadas.languages['EN']==None
        assert lampadas.languages['EN'].Supported
        assert lampadas.languages['EN'].I18n['EN'].Name=='English'
        assert lampadas.languages['FR'].Supported
        assert lampadas.languages['FR'].I18n['EN'].Name=='French'
        assert lampadas.languages.count()==136
        log(3, 'testing Languages done')


class testPubStatuses(unittest.TestCase):

    def testPubStatuses(self):
        log(3, 'testing PubStatuses')
        assert not lampadas.pub_statuses==None
        assert lampadas.pub_statuses.count() > 0
        assert not lampadas.pub_statuses['A']==None
        assert not lampadas.pub_statuses['A'].I18n==None
        assert not lampadas.pub_statuses['A'].I18n['EN']==None
        assert lampadas.pub_statuses['A'].I18n['EN'].Name > ''
        assert lampadas.pub_statuses['A'].I18n['EN'].Description > ''
        log(3, 'testing PubStatuses done')
        

class testTopics(unittest.TestCase):

    def testTopics(self):
        log(3, 'testing Topics')
        assert not lampadas.Topics==None
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
        assert not lampadas.Users==None
        assert lampadas.Users.count() > 0

        db.runsql("DELETE FROM username where email='foo@example.com'")
        db.commit()
    
        self.Oldid = db.read_value('SELECT MAX(user_id) from username')
        self.Newid = lampadas.Users.add('testuser', 'j', 'random', 'hacker', 'foo@example.com', 1, 1, 'pw', 'notes go here', 'default')
        assert self.Newid > 0
        assert self.Oldid + 1==self.Newid
        
        self.User = lampadas.User(self.Newid)
        assert not self.User==None
        assert self.User.id==self.Newid
        assert self.User.Username=='testuser'
        assert self.User.Email=='foo@example.com'
        
        lampadas.Users.Del(self.Newid)
        self.Newid = db.read_value('SELECT MAX(user_id) from username')
        assert self.Newid==self.Oldid
        log(3, 'testing Users done')


class testUserDocs(unittest.TestCase):

    def testUserDocs(self):
        log(3, 'testing UserDocs')
        self.User = lampadas.User(11)
        assert len(self.User.Docs) > 0
        assert self.User.Docs.count() > 0
        assert not self.User.Docs==None
        for UserDoc in self.User.Docs:
            assert not UserDoc==None
            assert not UserDoc.doc_id==None
            assert UserDoc.doc_id > 0
            assert UserDoc.Active==1 or UserDoc.Active==0
        log(3, 'testing UserDocs done')


class testUserDocs(unittest.TestCase):

    def testUserDocs(self):
        log(3, 'testing UserDocs')
        self.User = lampadas.User(11)
        assert len(self.User.Docs) > 0
        assert self.User.Docs.count() > 0
        assert not self.User.Docs==None
        for UserDoc in self.User.Docs:
            assert not UserDoc==None
            assert not UserDoc.doc_id==None
            assert UserDoc.doc_id > 0
            assert UserDoc.Active==1 or UserDoc.Active==0
            assert UserDoc.id==UserDoc.doc_id
        log(3, 'testing UserDocs done')


class testURLParse(unittest.TestCase):
    """
    FIXME: not all attributes of the URI object are tested... is this ok? --nico
    """

    def check_uri(self, url, result) :
        uri = URI(url)
        u = (uri.protocol, uri.server, uri.port, uri.path, uri.lang, uri.force_lang,
             uri.id, uri.format, uri.filename, uri.parameter, uri.anchor)
        self.assertEqual( (url,u), (url,result) )
        
    def testURLParse(self):
        # uri protocol server port path language
        # forcelang id format filename parameter anchor
        self.check_uri('',
                       ('',     '',        '',    '/','EN',0,0,'','home',   '',''))

        self.check_uri('/',
                       ('',     '',        '',    '/','EN',0,0,'','home',   '',''))

        self.check_uri('/home',
                       ('',     '',        '',    '/','EN',0,0,'','home',   '',''))

        self.check_uri('FR',
                       ('',     '',        '',    '/','FR',1,0,'','home',   '',''))

        self.check_uri('FR/',
                       ('',     '',        '',    '/','FR',1,0,'','home',   '',''))

        self.check_uri('FR/home',
                       ('',     '',        '',    '/','FR',1,0,'','home',   '',''))

        self.check_uri('/editdoc/1',
                       ('',     '',        '',    '/','EN',0,1,'','editdoc','',''))

        self.check_uri('ES/editdoc/1',
                       ('',     '',        '',    '/','ES',1,1,'','editdoc','',''))

        self.check_uri('http://localhost:8000',
                       ('http','localhost','8000','/','EN',0,0,'','home',   '',''))

        self.check_uri('http://localhost/editdoc/1',
                       ('http','localhost','',    '/','EN',0,1,'','editdoc','',''))

        self.check_uri('http://localhost/ES/editdoc/1',
                       ('http','localhost','',    '/','ES',1,1,'','editdoc','',''))

        self.check_uri('http://localhost:8000/ES/editdoc/1',
                       ('http','localhost','8000','/','ES',1,1,'','editdoc','',''))

        # FIXME: I added this one, is it ok? --nico
        self.check_uri('/home/file',
                       ('',     '',        '', 'home','EN',0,0,'','file',   '',''))


if __name__=="__main__":
	unittest.main()
