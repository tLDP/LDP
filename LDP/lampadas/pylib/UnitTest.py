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
from SourceFiles import sourcefiles
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
        assert not lampadas.types==None
        assert lampadas.types.count() > 0
        log(3, 'testing types done')


class testDocs(unittest.TestCase):

    def testDocs(self):
        log(3, 'testing Docs')
        assert not lampadas.docs==None
        assert lampadas.docs.count() > 0

        doc = lampadas.docs.add('Test Document',
                                'Test Doc',
                                'howto',
                                'xml',
                                'DocBook',
                                '4.1.2',
                                '1.0',
                                '2002-04-04',
                                'ISBN',
                                'N',
                                'N',
                                '2002-04-05',
                                '2002-04-10',
                                'N',
                                'gfdl',
                                '2.0',
                                'Copyright Holder',
                                'This is an abstract.',
                                'This is a short description.',
                                'EN',
                                'fooseries',
                                0)

        assert not doc==None
        assert doc.title=='Test Document'
        assert doc.format_code=='xml'
        
        title = doc.title
        doc.title = 'Foo'
        assert doc.title=='Foo'
        doc.save()
        
        lampadas.docs.delete(doc.id)

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
            if doc.errors.count() > 0:
                log(3, "found a doc with errors")
                for err_id in doc.errors.keys():
                    error = doc.errors[err_id]
                    assert not error==None
                    assert error.doc_id==doc.id
                    assert error.err_id > 1
        log(3, 'testing DocErrs done')
    

class testDocFiles(unittest.TestCase):

    def testDocFiles(self):
        log(3, 'testing DocFiles')
        keys = lampadas.docs.keys()
        for key in keys:
            doc = lampadas.docs[key]
            docfilekeys = doc.files.keys()
            for docfilekey in docfilekeys:
                docfile = doc.files[docfilekey]
                sourcefile = sourcefiles[docfilekey]
                if docfile==None: break
                assert docfile.doc_id==doc.id
                assert docfile.filename > ''
                assert docfile.filename==sourcefile.filename
        log(3, 'testing DocFiles done')


class testDocRatings(unittest.TestCase):

    def testDocRatings(self):
        log(3, 'testing DocRatings')
        dockeys = lampadas.docs.keys()
        for dockey in dockeys:

            doc = lampadas.docs[dockey]
            assert not doc==None
            doc.ratings.clear()
            doc.calc_rating()
            assert doc.ratings.count()==0
            assert doc.rating==0

            # Add Userid: 1   Rating: 5   -- Avg: 5

            doc.ratings.add('david', 5)
            doc.calc_rating()
            assert doc.ratings.count()==1
            assert doc.rating==5

            # Add Userid: 2   Rating: 7   -- Avg: 6
            
            doc.ratings.add('admin', 7)
            doc.calc_rating()
            assert doc.ratings.count()==2
            assert doc.rating==6

            # Del Userid: 1
        
            doc.ratings.delete('david')
            doc.calc_rating()
            assert doc.ratings.count()==1
            assert doc.rating==7

            # Clear again

            doc.ratings.clear()
            doc.calc_rating()
            assert doc.ratings.count()==0
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
            assert topic.name['EN'] > ''
        log(3, 'testing Topics done')


class testUsers(unittest.TestCase):

    def testUsers(self):
        log(3, 'testing Users')
        assert not lampadas.users==None

        count = lampadas.users.count()
        assert count > 0

        user = lampadas.users.add('testuser', 'j', 'random', 'hacker', 'foo@example.com', 1, 1, 'pw', 'notes go here', 'default')
        assert not user==None
        assert user.username=='testuser'
        assert user.email=='foo@example.com'
        
        lampadas.users.delete(user.username)
        assert lampadas.users.count()==count
        log(3, 'testing Users done')


class testUserDocs(unittest.TestCase):

    def testUserDocs(self):
        log(3, 'testing UserDocs')
        user = lampadas.user('david')
        assert len(user.docs) > 0
        assert user.docs.count() > 0
        assert not user.docs==None
        for key in user.docs.keys():
            userdoc = user.docs[key]
            assert not userdoc==None
            assert not userdoc.doc_id==None
            assert userdoc.doc_id > 0
            assert userdoc.active==1 or userdoc.active==0
        log(3, 'testing UserDocs done')


class testURLParse(unittest.TestCase):
    """
    FIXME: not all attributes of the URI object are tested... is this ok? --nico
    """

    def check_uri(self, url, result) :
        uri = URI(url)
        u = (uri.protocol, uri.server, uri.port, uri.path, uri.lang_ext, 
             uri.id, uri.code, uri.page_code, uri.parameter, uri.anchor)
        self.assertEqual( (url,u), (url,result) )
        
    def testURLParse(self):
        # uri protocol server port path language
        # forcelang id format filename parameter anchor
        self.check_uri('',
                       ('',     '',        '',    '/','.html',    0, '', 'index',  '',''))

        self.check_uri('/',
                       ('',     '',        '',    '/','.html',    0, '', 'index',   '',''))

        self.check_uri('/home.html',
                       ('',     '',        '',    '/','.html',    0, '', 'home',   '',''))

        self.check_uri('/home.fr.html',
                       ('',     '',        '',    '/','.fr.html', 0, '', 'home',   '',''))

        self.check_uri('/document_main/1.html',
                       ('',     '',        '',    '/','.html',    1, '', 'document_main','',''))

        self.check_uri('/document_main/1.es.html',
                       ('',     '',        '',    '/','.es.html', 1, '', 'document_main','',''))

        self.check_uri('http://localhost:8000',
                       ('http','localhost','8000','/','.html',    0, '', 'index',   '',''))

        self.check_uri('http://localhost/document_main/1.html',
                       ('http','localhost','',    '/','.html',    1, '', 'document_main','',''))

        self.check_uri('http://localhost/document_main/1.es.html',
                       ('http','localhost','',    '/','.es.html', 1, '', 'document_main','',''))

        self.check_uri('http://localhost:8000/document_main/1.es.html',
                       ('http','localhost','8000','/','.es.html', 1, '', 'document_main','',''))


if __name__=="__main__":
	unittest.main()
