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


class testTypes(unittest.TestCase):

    def testTypes(self):
        log(3, 'testing types')
        assert not lampadas.Types==None
        assert lampadas.types.count() > 0
        log(3, 'testing types done')


class testDocs(unittest.TestCase):

    def testDocs(self):
        log(3, 'testing Docs')
        assert not lampadas.docs==None
        assert lampadas.docs.count() > 0

        db.runsql("DELETE FROM document where title='testharness'")
        db.commit()
    
        old_id = db.read_value('SELECT max(doc_id) from document')
        new_id = lampadas.docs.add('testharness',
                                   'howto',
                                   'xml',
                                   'DocBook',
                                   '4.1.2',
                                   '1.0',
                                   '2002-04-04',
                                   'http://www.example.com/HOWTO.html',
                                   'ISBN',
                                   'N',
                                   'N',
                                   '2002-04-05',
                                   '2002-04-10',
                                   'http://www.home.com',
                                   'N',
                                   'gfdl',
                                   'This is a document.',
                                   'EN',
                                   'fooseries')
        assert new_id > 0
        assert old_id + 1==Newid

        doc = lampadas.docs[new_id]
        assert not doc==None
        assert doc.id==Newid
        assert doc.title=='testharness'
        assert doc.format_code=='xml'
        
        title = doc.title
        doc.title = 'Foo'
        assert doc.title=='Foo'
        doc.save()
        doc2 = lampadas.docs[new_id]
        assert doc2.title=='Foo'
        
        doc.title = title
        assert doc.title==title
        doc.save()
        assert doc.title==title
        doc2 = lampadas.docs[new_id]
        assert doc2.title==title
        
        lampadas.docs.delete(new_id)
        new_id = db.read_value('SELECT MAX(doc_id) from document')
        assert new_id==old_id

        keys = lampadas.docs.keys()
        for key in keys:
            doc = lampadas.docs[key]
            assert doc.id==key

        log(3, 'testing Docs done')


class testDocErrs(unittest.TestCase):

    def testDocErrs(self):
        log(3, 'testing DocErrs')
        keys = lampadas.docs.keys()
        for key in keys:
            doc = lampadas.docs[key]
            assert not doc==None
            if doc.errs.count() > 0:
                log("found a doc with errors")
                for err in doc.errs:
                    assert not err==None
                    assert err.doc_id==doc.id
                    assert err.err_id > 1
        log(3, 'testing DocErrs done')
    

class testDocFiles(unittest.TestCase):

    def testDocFiles(self):
        log(3, 'testing DocFiles')
        keys = lampadas.docs.keys()
        for key in keys:
            filekeys = doc.files.keys()
            for filekey in filekeys:
                file = Doc.files[filekey]
                if file==None: break
                assert file.doc_id==doc.id
                assert file.filename > ''
        log(3, 'testing DocFiles done')


class testDocRatings(unittest.TestCase):

    def testDocRatings(self):
        log(3, 'testing DocRatings')
        dockeys = lampadas.docs.keys()
        for dockey in dockeys:

            doc = lampadas.docs[dockey]
            assert not doc==None
            doc.ratings.clear()
            assert doc.ratings.count()==0
            assert doc.rating==0

            # Add Userid: 1   Rating: 5   -- Avg: 5

            doc.ratings.add(1, 5)
            assert doc.ratings.count()==1
            assert doc.ratings.average==5
            assert doc.rating==5

            # Add Userid: 2   Rating: 7   -- Avg: 6
            
            doc.ratings.add(2, 7)
            assert doc.ratings.count()==2
            assert doc.ratings.average==6
            assert doc.rating==6

            # Del Userid: 1
        
            doc.ratings.delete(1)
            assert doc.ratings.count()==1
            assert doc.ratings.average==7
            assert doc.rating==7

            # Clear again

            doc.ratings.clear()
            assert doc.ratings.count()==0
            assert doc.ratings.average==0
            assert doc.rating==0
        log(3, 'testing DocRatings done')


class testDocVersions(unittest.TestCase):

    def testDocVersions(self):
        log(3, 'testing DocVersions')
        keys = lampadas.docs.keys()
        found = 0
        for key in keys:
            doc = lampadas.docs[key]
            assert not doc==None
            if doc.versions.count() > 0:
                found = 1
                vkeys = doc.versions.keys()
                for vkey in vkeys:
                    version = doc.versions[vkey]
                    assert not version==None
                    assert version.pub_date > ''
                    assert version.initials > ''
        assert found==1
        log(3, 'testing DocVersions done')


class testLicenses(unittest.TestCase):

    def testLicenses(self):
        log(3, 'testing Licenses')
        assert lampadas.licenses.count() > 0
        assert not lampadas.licenses['gpl']==None
        log(3, 'testing Licenses done')


class test_dtds(unittest.TestCase):

    def test_dtds(self):
        log(3, 'testing DTDs')
        assert lampadas.dtds.count() > 0
        assert not lampadas.dtds['DocBook']==None
        log(3, 'testing DTDs done')


class testFormats(unittest.TestCase):

    def testFormats(self):
        log(3, 'testing Formats')
        assert lampadas.formats.count() > 0
        assert not lampadas.formats['xml']==None
        assert lampadas.formats['xml'].name['EN'] > ''
        assert lampadas.formats['xml'].description['EN'] > ''
        log(3, 'testing Formats done')


class testLanguages(unittest.TestCase):

    def testLanguages(self):
        log(3, 'testing Languages')
        assert not lampadas.languages==None
        assert not lampadas.languages['EN']==None
        assert lampadas.languages['EN'].supported
        assert lampadas.languages['EN'].name['EN']=='English'
        assert lampadas.languages['FR'].supported
        assert lampadas.languages['FR'].name['EN']=='French'
        assert lampadas.languages['DE'].supported
        assert lampadas.languages['DE'].name['EN']=='German'
        assert lampadas.languages.count()==136
        log(3, 'testing Languages done')


class testPubStatuses(unittest.TestCase):

    def testPubStatuses(self):
        log(3, 'testing PubStatuses')
        assert not lampadas.pub_statuses==None
        assert lampadas.pub_statuses.count() > 0
        assert not lampadas.pub_statuses['A']==None
        assert lampadas.pub_statuses['A'].name['EN'] > ''
        assert lampadas.pub_statuses['A'].description['EN'] > ''
        log(3, 'testing PubStatuses done')
        

class testTopics(unittest.TestCase):

    def testTopics(self):
        log(3, 'testing Topics')
        assert not lampadas.topics==None
        assert lampadas.topics.count() > 0
        keys = lampadas.topics.keys()
        for key in keys:
            topic = lampadas.topics[key]
            assert topic.num > 0
            assert topic.name['EN'] > ''
            assert topic.description['EN'] > ''
        log(3, 'testing Topics done')


class testUsers(unittest.TestCase):

    def testUsers(self):
        log(3, 'testing Users')
        assert not lampadas.users==None
        assert lampadas.users.count() > 0

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
             uri.id, uri.code, uri.filename, uri.parameter, uri.anchor)
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
