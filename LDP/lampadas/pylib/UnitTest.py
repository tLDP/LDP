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

This module runs a series of tests on the Python modules,
looking for anything that breaks. It is used for regression
testing before committing changes into CVS.

NOTICE: You must always run the UnitTest.py module before
checking your changes into the CVS tree. Remember, other
developers are working on the codebase too, and they will
not appreciate it if their work is interrupted because the CVS
tree is broken.
"""

import unittest
from Config import config
from Database import db
from Languages import languages
from Docs import docs
from Users import users, User
from Types import types
from Licenses import licenses
from DTDs import dtds
from Formats import formats
from PubStatuses import pub_statuses
from Topics import topics
from SourceFiles import sourcefiles
from URLParse import URI
from Log import log
import os

BIN = '/home/david/ldp/csv/LDP/lampadas/bin/'
PYLIB = '/home/david/ldp/csv/LDP/lampadas/bin/'
EXTERNAL_TESTS = (BIN + 'rebuild', BIN + 'reload', 'Lintadas.py', 'Mirror.py', 'Makefile.py publish')
EXTERNAL_TESTS = (BIN + 'rebuild', BIN + 'reload')

# TESTS TO ADD:
# 
# make sure there are no conflicts between blocks and strings, which could
# confuse things.

# Unit Tests ###################################################################


class testTypes(unittest.TestCase):

    def testTypes(self):
        log(3, 'testing types')
        assert not types==None
        assert types.count() > 0
        log(3, 'testing types done')


class testDocs(unittest.TestCase):

    def testDocs(self):
        log(3, 'testing Docs')

        # Add
        doc = docs.add('Test Document',
                                'Test Doc',
                                'howto',
                                'xml',
                                'docbook',
                                '4.1.2',
                                '1.0',
                                '2002-04-04',
                                'ISBN',
                                'UTF-8',
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
                                0,
                                '2002-01-01 15:35:21',
                                '2002-02-02 15:35:22',
                                '2002-03-03 15:35:23',
                                '2002-01-01 12:12:12')

        assert not doc==None
        assert doc.title=='Test Document'
        assert doc.short_title=='Test Doc'
        assert doc.type_code=='howto'
        assert doc.format_code=='xml'
        assert doc.dtd_code=='docbook'
        
        title = doc.title
        doc.title = 'Foo'
        assert doc.title=='Foo'
        doc.save()
       
        # Delete
        docs.delete(doc.id)
        assert docs[doc.id]==None

        keys = docs.keys()
        for key in keys:
            doc = docs[key]
            assert doc.id==key

        log(3, 'testing Docs done')


class testDocErrs(unittest.TestCase):

    def testDocErrs(self):
        log(3, 'testing DocErrs')
        keys = docs.keys()
        for key in keys:
            doc = docs[key]
            assert not doc==None
            if doc.errors.count() > 0:
                log(3, "found a doc with errors")
                for err_id in doc.errors.keys():
                    error = doc.errors[err_id]
                    assert not error==None
                    assert error.doc_id==doc.id
                    assert error.err_id > 0
        log(3, 'testing DocErrs done')
    

class testDocFiles(unittest.TestCase):

    def testDocFiles(self):
        log(3, 'testing DocFiles')
        keys = docs.keys()
        for key in keys:
            doc = docs[key]
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
        dockeys = docs.keys()
        for dockey in dockeys:

            doc = docs[dockey]
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
        keys = docs.keys()
        found = 0
        for key in keys:
            doc = docs[key]
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
        assert licenses.count() > 0
        assert not licenses['gpl']==None
        log(3, 'testing Licenses done')


class test_dtds(unittest.TestCase):

    def test_dtds(self):
        log(3, 'testing DTDs')
        assert dtds.count() > 0
        assert not dtds['docbook']==None
        log(3, 'testing DTDs done')


class testFormats(unittest.TestCase):

    def testFormats(self):
        log(3, 'testing Formats')
        assert formats.count() > 0
        assert not formats['xml']==None
        assert formats['xml'].name['EN'] > ''
        assert formats['xml'].description['EN'] > ''
        log(3, 'testing Formats done')


class testLanguages(unittest.TestCase):

    def testLanguages(self):
        log(3, 'testing Languages')
        assert not languages==None
        assert not languages['EN']==None
        assert languages['EN'].supported
        assert languages['EN'].name['EN']=='English'
        assert languages['FR'].supported
        assert languages['FR'].name['EN']=='French'
        assert languages['DE'].supported
        assert languages['DE'].name['EN']=='German'
        assert languages.count()==136
        log(3, 'testing Languages done')


class testPubStatuses(unittest.TestCase):
    
    def testPubStatuses(self):
        log(3, 'testing PubStatuses')
        assert not pub_statuses==None
        assert pub_statuses.count() > 0
        
        # Ensure that the default publication statuses are in the database
        # for all supported languages, and that they all have names and
        # descriptions.
        for pub_status in ('C', 'D', 'N', 'P', 'W'):
            assert not pub_statuses[pub_status]==None
            for lang in languages.supported_keys('EN'):
                assert pub_statuses[pub_status].name[lang] > ''
                assert pub_statuses[pub_status].description[lang] > ''
        log(3, 'testing PubStatuses done')
        

class testTopics(unittest.TestCase):

    def testTopics(self):
        log(3, 'testing Topics')
        assert not topics==None
        assert topics.count() > 0
        keys = topics.keys()
        for key in keys:
            topic = topics[key]
            assert topic.name['EN'] > ''
        log(3, 'testing Topics done')


class testUsers(unittest.TestCase):

    def testUsers(self):
        log(3, 'testing Users')
        assert not users==None

        count = users.count()
        assert count > 0

        user = users.add('testuser', 'j', 'random', 'hacker', 'foo@example.com', 1, 1, 'pw', 'notes go here')
        assert not user==None
        assert user.username=='testuser'
        assert user.email=='foo@example.com'
        
        users.delete(user.username)
        assert users.count()==count
        log(3, 'testing Users done')


class testUserDocs(unittest.TestCase):

    def testUserDocs(self):
        log(3, 'testing UserDocs')
        user = User('david')
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
        #              uri
        #               protocol server       port    path lang_ext    id code page            param anchor
        # format filename parameter anchor
        self.check_uri('',
                       ('',      '',          '',     '/', '.en.html', 0, '', 'index',         '',   ''))

        self.check_uri('/',
                       ('',      '',          '',     '/', '.en.html', 0, '', 'index',         '',   ''))

        self.check_uri('/home.html',
                       ('',      '',          '',     '/', '.en.html', 0, '', 'home',          '',   ''))

        self.check_uri('/home.fr.html',
                       ('',      '',          '',     '/', '.fr.html', 0, '', 'home',          '',   ''))

        self.check_uri('/document_main/1.html',
                       ('',      '',          '',     '/', '.en.html', 1, '', 'document_main', '',   ''))

        self.check_uri('/document_main/1.es.html',
                       ('',      '',          '',     '/', '.es.html', 1, '', 'document_main', '',   ''))

        self.check_uri('http://localhost:8000',
                       ('http',  'localhost', '8000', '/', '.en.html', 0, '', 'index',         '',   ''))

        self.check_uri('http://localhost/document_main/1.html',
                       ('http',  'localhost', '',     '/', '.en.html', 1, '', 'document_main', '',   ''))

        self.check_uri('http://localhost/document_main/1.es.html',
                       ('http',  'localhost', '',     '/', '.es.html', 1, '', 'document_main', '',   ''))

        self.check_uri('http://localhost:8000/document_main/1.es.html',
                       ('http',  'localhost', '8000', '/', '.es.html', 1, '', 'document_main', '',   ''))


if __name__=="__main__":
    log(3, 'testing commands')
    for command in EXTERNAL_TESTS:
        log(3, 'testing command: ' + command)
        os.system(command)
        log(3, 'testing command: ' + command + ' done')
    log(3, 'testing commands done')

	unittest.main()
