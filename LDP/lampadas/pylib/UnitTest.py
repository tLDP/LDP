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
from Globals import *
from URLParse import URI
from Log import log

import datamanager
import persistence

dms = datamanager.DataManagers()
dms.set_object_classes(persistence)

print 'Preloading data...'
blocks = dms.document.get_all()
collections = dms.collection.get_all
docs = dms.document.get_by_keys([['doc_id', '<=', 10000]])
dtds = dms.dtd.get_by_keys([['dtd_code', '<>', 'FOO_DTD']])
encodings = dms.encoding.get_all()
errors = dms.error.get_all()
error_types = dms.error_type.get_all()
formats = dms.format.get_all()
languages = dms.language.get_all()
licenses = dms.license.get_all()
news = dms.news.get_all()
pages = dms.page.get_all()
pub_statuses = dms.pub_status.get_all()
review_status = dms.review_status.get_all()
roles = dms.role.get_all()
sections = dms.section.get_all()
sessions = dms.session.get_all()
sourcefiles = dms.sourcefile.get_all()
templates = dms.template.get_all()
topics = dms.topic.get_all()
types = dms.type.get_all()
users = dms.username.get_all()
webstrings = dms.webstring.get_all()
print 'Done.'

BIN = '/home/david/ldp/cvs/LDP/lampadas/bin/'
EXTERNAL_TESTS = [BIN + 'rebuild', BIN + 'reload', 'Lintadas.py', 'Mirror.py', 'Makefile.py publish']
EXTERNAL_TESTS = [BIN + 'rebuild', BIN + 'reload']
#
## TESTS TO ADD:
## 
## make sure there are no conflicts between blocks and strings, which could
## confuse things.
#
## Unit Tests ###################################################################
#
#
class testTypes(unittest.TestCase):

    def testTypes(self):
        log(3, 'testing types')
        assert not types==None
        assert types.count() > 0
        log(3, 'testing types done')


class testDocs(unittest.TestCase):

    def testDocs(self):
        log(3, 'testing Docs')

        doc = dms.document.get_by_id(50000)
        assert doc==None, 'When calling docs[id] with a nonexistent id, I got back a doc!'

        # Add
        doc = dms.document.new()
        doc.title                  = 'Test Document'
        doc.short_title            = 'Test Doc'
        doc.type_code              = 'howto'
        doc.format_code            = 'xml'
        doc.dtd_code               = 'docbook'
        doc.dtd_version            = '4.1.2'
        doc.version                = '1.0'
        doc.last_update            = '2002-04-04'
        doc.isbn                   = 'ISBN'
        doc.encoding               = 'UTF-8'
        doc.pub_status_code        = 'N'
        doc.review_status_code     = 'N'
        doc.tickle_date            = '2002-04-05'
        doc.pub_date               = '2002-04-10'
        doc.tech_review_staus_code = 'N'
        doc.maintained             = 1
        doc.maintainer_wanted      = 0
        doc.license_code           = 'gfdl'
        doc.license_version        = '2.0'
        doc.copyright_holder       = 'Copyright Holder'
        doc.abstract               = 'This is an abstract.'
        doc.short_desc             = 'This is a short description.'
        doc.rating                 = 5
        doc.lang                   = 'EN'
        doc.sk_seriesid            = 'fooseries'
        doc.replaced_by_id         = 0
        doc.lint_time              = '2002-01-01 15:35:21'
        doc.mirror_time            = '2002-02-02 15:35:22'
        doc.pub_time               = '2002-03-03 15:35:23'
        doc.first_pub_date         = '2002-01-01 12:12:12'

        doc.save()
        assert doc.id > 0
        assert doc.title=='Test Document'
        assert doc.short_title=='Test Doc'
        assert doc.type_code=='howto'
        assert doc.format_code=='xml'
        assert doc.dtd_code=='docbook'
        assert not doc==None
        
        title = doc.title
        doc.title = 'Foo'
        assert doc.title=='Foo'
        
        # Test the alternate save route -- directly through the object.
        doc_id = doc.id
        doc.save()
        doc2 = dms.document.get_by_id(doc_id)
        assert doc2.id==doc_id
       
        # Delete
        doc_id = doc.id
        dms.document.delete(doc)
        
        doc = dms.document.get_by_id(doc_id)
        assert doc==None

        keys = docs.keys()
        for key in keys:
            doc = docs[key]
            assert doc.id==key

        log(3, 'testing Docs done')


class testDocTopics(unittest.TestCase):

    def testDocTopics(self):
        keys = docs.keys()
        for key in keys:
            doc = docs[key]
            assert not doc==None
#            print 'Testing topics for document %s' % doc.id
#            print 'Doc has %s topics' % doc.topics.count()
            if doc.topics.count() > 0:
                dtkeys = doc.topics.keys('doc_id')
                for dtkey in dtkeys:
                    assert dtkey==doc.id
                for dtkey in doc.topics.keys():
#                    print 'Testing topic %s' % topic_code
                    doctopic = doc.topics[dtkey]
                    assert not doctopic==None
                    assert doctopic.doc_id==doc.id, 'doctopic.doc_id doesn\'t match doc.id: ' + str(doctopic.doc_id) + ', ' + str(doc.id)
                    assert doctopic.topic_code > ''

        assert topics.count() > 0
        doc = docs[1]
        assert not doc==None
        remember_topics = dms.document_topic.get_by_keys([['doc_id', '=', doc.id]])
        remember_count = doc.topics.count()
        assert len(remember_topics)==doc.topics.count()
#        print 'Clearing ' + str(remember_count) + ' topics...'
#        print doc.topics.keys()
        doc.topics.clear()
        assert doc.topics.count()==0, 'doc.topics should be clear, but has ' + str(doc.topics.count()) + ' items.'
        for topic_code in topics.keys():
            doctopic = doc.topics.new()
            doctopic.doc_id = doc.id
            doctopic.topic_code = topic_code
            doc.topics.add(doctopic)
            doctopic = doc.topics[doctopic.topic_code]
#            print doctopic.where()
#            print doctopic.parent
        assert doc.topics.count()==topics.count(), 'Counts don\'t match: %s and %s ' % (doc.topics.count(), topics.count())
        for key in doc.topics.keys():
            doc.topics.delete(doc.topics[key])
        assert doc.topics.count()==0, 'doc.topics should be clear, but has ' + str(doc.topics.count()) + ' items.'
        count = 0
#        print 'doctopics is: ' + str(doctopics)
        for key in remember_topics.keys():
            doctopic = dms.document_topic.new()
            doctopic.doc_id = doc.id
            doctopic.topic_code = remember_topics[key].topic_code
#            print 'doc.topics is: ' + str(doc.topics) + ', parent is: ' + str(doc.topics.parent_collection)
            doc.topics.add(doctopic)
#            print 'Added back ' + topic_code
            count += 1
        assert doc.topics.count()==count
        assert doc.topics.count()==remember_count

class testDocErrs(unittest.TestCase):

    def testDocErrs(self):
        log(3, 'testing DocErrs')
        
        limit = 50
        keys = docs.keys()
        for key in keys:
            limit = limit - 1
            if limit==0:
                break
            doc = docs[key]
            assert not doc==None
            docerrors = doc.errors
            if docerrors.count() > 0:
                log(3, "found a doc with errors")
                for docerrkey in docerrors.keys():
                    docerr = docerrors[docerrkey]
                    assert not docerr==None
                    assert docerr.doc_id==doc.id
                    assert docerr.err_id > 0
                    err = errors[docerr.err_id]
                    assert not err==None
                    assert err.id==docerr.err_id
                    assert err.err_type_code==docerr.err_type_code
            else:
                newerr = dms.document_error.new()
                newerr.doc_id =doc.id
                newerr.err_id = ERR_NO_SOURCE_FILE
                newerr.notes  = ''
                doc.errors.add(newerr)
                assert doc.errors.count()==1, 'doc.errors.count() should be 1, but has ' + str(doc.errors.count()) + ' items.'
                doc.errors.delete(newerr)
                assert doc.errors.count()==0, 'doc.errors.count() should be 0, but has ' + str(doc.errors.count()) + ' items.'
        log(3, 'testing DocErrs done')
    

class testSourcefiles(unittest.TestCase):

    def testSourcefiles(self):
        log (3, 'testing Sourcefiles')
        for key in sourcefiles.keys():
            sourcefile = sourcefiles[key]
            for key in sourcefile.documents.keys():
                docfile = sourcefile.documents[key]
                assert docfile.filename==sourcefile.filename
            for key in sourcefile.errors.keys():
                docerr = sourcefile.errors[key]
                assert docerr.filename==sourcefile.filename
        log (3, 'testing Sourcefiles done')

        
class testDocFiles(unittest.TestCase):

    def testDocFiles(self):
        log(3, 'testing DocFiles')
        
        for key in docs.keys():
            doc = docs[key]
            docfiles = doc.files
            for docfilekey in docfiles.keys():
                docfile = docfiles[docfilekey]
                sourcefile = sourcefiles[docfile.filename]
                if docfile==None: break
                assert docfile.doc_id==doc.id
                assert docfile.filename > ''
                assert docfile.filename==sourcefile.filename
                assert docfile.filename==docfile.sourcefile.filename
        log(3, 'testing DocFiles done')


class testDocRatings(unittest.TestCase):

    def testDocRatings(self):
        log(3, 'testing DocRatings')
        doc = docs[1]
        assert not doc==None
        doc.ratings.clear()
        assert doc.ratings.count()==0, 'doc.ratings.count() should be 0, but has ' + str(doc.ratings.count()) + ' items.'
        assert doc.ratings.average('rating')==0

        # Add Userid: 1   Rating: 5   -- Avg: 5

        docrating = dms.document_rating.new()
        docrating.doc_id = doc.id
        docrating.rating = 5
        docrating.username = 'david'
        doc.ratings.add(docrating)
        assert doc.ratings.count()==1
        assert doc.ratings.average('rating')==5
        set = dms.document_rating.get_by_keys([['username', '=', 'david'], ['doc_id', '=', doc.id]])
        assert set.count()==1
        assert set.average('rating')==5

        # Add Userid: 2   Rating: 7   -- Avg: 6
        
        docrating = dms.document_rating.new()
        docrating.doc_id = doc.id
        docrating.rating = 7
        docrating.username = 'admin'
        doc.ratings.add(docrating)
        assert doc.ratings.count()==2
        assert doc.ratings.average('rating')==6
        set = dms.document_rating.get_by_keys([['doc_id', '=', doc.id]])
        assert set.count()==2
        assert set.average('rating')==6

        # Del Userid: 1
    
        doc.ratings.delete_by_keys([['username', '=', 'david']])
        assert doc.ratings.count()==1
        assert doc.ratings.average('rating')==7

        # Clear again

        doc.ratings.clear()
        assert doc.ratings.count()==0
        assert doc.ratings.average('rating')==0
        log(3, 'testing DocRatings done')


class testDocVersions(unittest.TestCase):

    def testDocVersions(self):
        log(3, 'testing DocVersions')

        found = 0
        for key in docs.keys():
            doc = docs[key]
            assert not doc==None
            if doc.versions.count() > 0:
                found = 1
                for vkey in doc.versions.keys():
                    version = doc.versions[vkey]
                    assert not version==None
                    assert version.pub_date > ''
                    assert version.initials > ''
        assert found==1
        log(3, 'testing DocVersions done')


class testDocUsers(unittest.TestCase):

    def testDocUsers(self):
        log(3, 'testing DocUsers')

        found = 0
        for key in docs.keys():
            doc = docs[key]
            assert not doc==None
            if doc.users.count() > 0:
                found = 1
                for ukey in doc.users.keys():
                    docuser = doc.users[ukey]
                    assert not docuser==None
                    assert docuser.username > ''
                    assert not docuser.user==None
                    assert docuser.username==docuser.user.username
        assert found==1
        log(3, 'testing DocUsers done')


class testLicenses(unittest.TestCase):

    def testLicenses(self):
        log(3, 'testing Licenses')
        assert licenses.count() > 0
        for key in licenses.keys():
            license = licenses[key]
            assert license.short_name['EN'] > ''
            assert license.name['EN'] > ''
            assert license.description['EN'] > ''
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
            supported = dms.language.get_by_keys([['supported', '=', YES]])
            for key in supported.keys():
                language = languages[key]
                assert pub_statuses[pub_status].name[language.code] > ''
                assert pub_statuses[pub_status].description[language.code] > ''
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

        user = users['testuser']
        if not user==None:
            users.delete(user)

        user = users['testuser']
        assert user==None
        
        count = users.count()
        assert count > 0

        user = dms.username.new()
        assert user.changed==0
        user.username    = 'testuser'
        assert user.changed==1
        user.first_name  = 'j'
        user.middle_name = 'random'
        user.surname     = 'hacker'
        user.email       = 'foo@example.com'
        user.admin       = 1
        user.sysadmin    = 1
        user.password    = 'pw'
        user.notes       = 'notes go here'
        assert user.in_database==0
        users.add(user)
        assert user.in_database==1
        assert user.key==user.username

        user = users['testuser']
        assert not user==None
        assert user.username=='testuser'
        assert user.email=='foo@example.com'
        
        users.delete(user)
        assert users.count()==count
        log(3, 'testing Users done')


class testUserDocs(unittest.TestCase):

    def testUserDocs(self):
        log(3, 'testing UserDocs')
        user = users['david']
        assert user.documents.count() > 0
        assert not user.documents==None
        for key in user.documents.keys():
            userdoc = user.documents[key]
            assert not userdoc==None
            assert not userdoc.doc_id==None
            assert userdoc.doc_id > 0
            assert userdoc.active==1 or userdoc.active==0
        log(3, 'testing UserDocs done')


class testSections(unittest.TestCase):

    def testUserDocs(self):
        log(3, 'testing Sections')
        for key in sections.keys():
            section = sections[key]
            assert section.static_count > -1
            assert section.nonregistered_count > -1
            assert section.nonadmin_count > -1
            assert section.nonsysadmin_count > -1
            assert section.name['EN'] > ''
        log(3, 'testing Sections done')


class testPages(unittest.TestCase):

    def testPages(self):
        log(3, 'testing Pages')
        for key in pages.keys():
            page = pages[key]
            assert page.menu_name['EN'] > ''
            assert page.title['EN'] > ''
            assert page.page['EN'] > ''
            assert page.version['EN'] > ''
            if page.section_code > '':
                assert not page.section==None
                assert page.section.code==page.section_code
            if page.template_code > '':
                assert not page.template==None
                assert page.template.code==page.template_code
        log(3, 'testing Pages done')

        
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


def print_cache_stats():
    print 'Cache statistics:'
    print '  blocks:          %s/%s' % (blocks.dms.cache.hits, blocks.dms.cache.misses)
    print '  collections:     %s/%s' % (collections.dms.cache.hits, collections.dms.cache.misses)
    print '  documents:       %s/%s' % (documents.dms.cache.hits, documents.dms.cache.misses)
    print '  dtds:            %s/%s' % (dtds.dms.cache.hits, dtds.dms.cache.misses)
    print '  errors:          %s/%s' % (errors.dms.cache.hits, errors.dms.cache.misses)
    print '  error_types:     %s/%s' % (error_types.dms.cache.hits, error_types.dms.cache.misses)
    print '  formats:         %s/%s' % (formats.dms.cache.hits, formats.dms.cache.misses)
    print '  languages:       %s/%s' % (languages.dms.cache.hits, languages.dms.cache.misses)
    print '  licenses:        %s/%s' % (licenses.dms.cache.hits, licenses.dms.cache.misses)
    print '  news:            %s/%s' % (news.dms.cache.hits, news.dms.cache.misses)
    print '  pages:           %s/%s' % (pages.dms.cache.hits, pages.dms.cache.misses)
    print '  pub_statuses:    %s/%s' % (pub_statuses.dms.cache.hits, pub_statuses.dms.cache.misses)
    print '  review_statuses: %s/%s' % (review_statuses.dms.cache.hits, review_statuses.dms.cache.misses)
    print '  roles:           %s/%s' % (roles.dms.cache.hits, roles.dms.cache.misses)
    print '  sections:        %s/%s' % (sections.dms.cache.hits, sections.dms.cache.misses)
    print '  sessions:        %s/%s' % (sessions.dms.cache.hits, sessions.dms.cache.misses)
    print '  sourcefiles:     %s/%s' % (sourcefiles.dms.cache.hits, sourcefiles.dms.cache.misses)
    print '  templates:       %s/%s' % (templates.dms.cache.hits, templates.dms.cache.misses)
    print '  topics:          %s/%s' % (topics.dms.cache.hits, topics.dms.cache.misses)
    print '  types:           %s/%s' % (types.dms.cache.hits, types.dms.cache.misses)
    print '  users:           %s/%s' % (users.dms.cache.hits, users.dms.cache.misses)
    print '  webstrings:      %s/%s' % (webstrings.dms.cache.hits, webstrings.dms.cache.misses)

if __name__=="__main__":
    log(3, 'testing commands')
    for command in EXTERNAL_TESTS:
        log(3, 'testing command: ' + command)
#        os.system(command)
        print command
        log(3, 'testing command: ' + command + ' done')
    log(3, 'testing commands done')
    unittest.main()
    print_cache_stats()
