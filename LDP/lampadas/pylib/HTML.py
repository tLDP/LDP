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
Lampadas HTML Primitives Module

This module generates HTML primitives and web pages for the WWW front-end
to the Lampadas system.
"""

# Modules ##################################################################

from Globals import *
from Config import config
from Log import log
from URLParse import URI
from DataLayer import *
from SourceFiles import sourcefiles
from WebLayer import lampadasweb
from Tables import tables
from Widgets import widgets
from Lintadas import lintadas
from Sessions import sessions
import commands
import string
import sys
import os
import time
import fpformat
import re

# Globals


# PageFactory

class PageFactory:

    elapsed_time = 0

    def page_exists(self, key):
        uri = URI(key)
        if uri.path=='' and lampadasweb.pages[uri.page_code]:
            return 1
        return

    def page(self, uri):
        if sessions.session:
            log(3, 'user: ' + sessions.session.username)

        page = lampadasweb.pages[uri.page_code]
        if page==None:
            page = lampadasweb.pages['404']
        assert not page==None
        html = self.build_page(page, uri)

        return html
    
    def build_page(self, page, uri):
        start_time = time.time()
        template = lampadasweb.templates[page.template_code]
        assert not template==None
        html = template.template

        html = self.replace_tokens(page, uri, html)

        end_time = time.time()
        self.elapsed_time = end_time - start_time
        html = html.replace('DCM_ELAPSED_TIME', fpformat.fix(self.elapsed_time, 3))
        html = html.replace('DCM_PIPE', '|')
        return html

    def replace_tokens(self, page, uri, html):
        temp = html.replace('\|', 'DCM_PIPE')
        pos = temp.find('|')
        while pos <> -1 :
            temp = temp.replace('\|', 'DCM_PIPE')
            pos2 = temp.find('|', pos+1)
            if pos2==-1:
                pos = -1
            else:
                token = temp[pos+1:pos2]

                newstring = None
            
                # System diagnostic tokens
                if token=='elapsed_time':
                    newstring = 'DCM_ELAPSED_TIME'
                    
                # Tokens based on a logged-in user
                elif token=='session_id':
                    if sessions.session:
                        newstring = sessions.session.user.session_id
                    else:
                        newstring = ''
                elif token=='session_username':
                    if sessions.session:
                        newstring = sessions.session.username
                    else:
                        newstring = ''
                elif token=='session_name':
                    if sessions.session:
                        newstring = sessions.session.user.name
                    else:
                        newstring = ''
                elif token=='session_user_docs':
                    if sessions.session:
                        newstring = tables.userdocs(uri, username=sessions.session.username)
                    else:
                        newstring = '|nopermission|'

                # Meta-data about the page being served
                elif token=='title':
                    newstring = page.title[uri.lang]
                elif token=='body':
                    if page.only_registered==1 and sessions.session==None:
                        newstring = '|blknopermission|'
                    elif page.only_admin==1 and (sessions.session==None or sessions.session.user.admin==0):
                        newstring = '|blknopermission|'
                    elif page.only_sysadmin==1 and (sessions.session==None or sessions.session.user.sysadmin==0):
                        newstring = '|blknopermission|'
                    else:
                        newstring = page.page[uri.lang]
                elif token=='base':
                    newstring = 'http://' + config.hostname
                    if config.port > '':
                        newstring = newstring + ':' + config.port
                    newstring = newstring + config.root_dir
                    if uri.force_lang:
                        newstring = newstring + uri.lang + '/'

                # Meta-data from the page's URL
                elif token=='uri.lang_ext':
                    newstring = uri.lang_ext
                elif token=='uri.base':
                    newstring = uri.base
                elif token=='uri.page_code':
                    newstring = uri.page_code
                elif token=='uri.id':
                    newstring = str(uri.id)
                elif token=='uri.code':
                    newstring = uri.code
                elif token=='uri.filename':
                    newstring = uri.filename


                # Configuration information
                elif token=='hostname':
                    newstring = config.hostname
                elif token=='rootdir':
                    newstring = config.root_dir
                elif token=='port':
                    newstring = str(config.port)
                elif token=='stylesheet':
                    if sessions.session:
                        newstring = sessions.session.user.stylesheet
                    else:
                        newstring='default'
                elif token=='version':
                    newstring = VERSION

                ###########################################
                # Tokens for when a page embeds an object #
                ###########################################
                
                # Embedded User
                elif token=='user.username':
                    if sessions.session:
                        newstring = sessions.session.username
                    else:
                        newstring = '|blknotfound|'
                elif token=='user.name':
                    if sessions.session:
                        newstring = user.name
                    else:
                        newstring = '|blknotfound|'
                elif token=='user.docs':
                    if sessions.session:
                        newstring = tables.userdocs(uri, uri.username)
                    else:
                        newstring = '|blknotfound|'

                # Embedded Type
                elif token=='type.name':
                    type = lampadas.types[uri.code]
                    if not type:
                        newstring = '|blknotfound|'
                    else:
                        newstring = type.name[uri.lang]

                # Embedded Topic
                elif token=='topic.name':
                    topic = lampadas.topics[uri.code]
                    if not topic:
                        newstring = '|blknotfound|'
                    else:
                        newstring = topic.name[uri.lang]
                elif token=='topic.description':
                    topic = lampadas.topics[uri.code]
                    if not topic:
                        newstring = '|blknotfound|'
                    else:
                        newstring = topic.description[uri.lang]

                # Navigation Boxes
                elif token=='navlogin':
                    newstring = tables.login(uri)
                elif token=='navmenus':
                    newstring = tables.section_menus(uri)
                elif token=='navtopics':
                    newstring = tables.topics(uri)
                elif token=='navtypes':
                    newstring = tables.types(uri)
                elif token=='navsessions':
                    newstring = tables.navsessions(uri)
                elif token=='navlanguages':
                    newstring = tables.languages(uri)

                # Tables
                elif token=='tabsubtopics':
                    newstring = tables.subtopics(uri)
                elif token=='tabdocs':
                    newstring = tables.doctable(uri, lang=uri.lang)
                elif token=='tabmaint_wanted':
                    newstring = tables.doctable(uri, maintainer_wanted=1, lang=uri.lang)
                elif token=='tabunmaintained':
                    newstring = tables.doctable(uri, maintained=0, lang=uri.lang)
                elif token=='tabpending':
                    newstring = tables.doctable(uri, pub_status_code='P', lang=uri.lang)
                elif token=='tabwishlist':
                    newstring = tables.doctable(uri, pub_status_code='W', lang=uri.lang)
                elif token=='tabeditdoc':
                    newstring = tables.doc(uri)
                elif token=='tabdocfiles':
                    newstring = tables.docfiles(uri)
                elif token=='tabdocusers':
                    newstring = tables.docusers(uri)
                elif token=='tabdocversions':
                    newstring = tables.docversions(uri)
                elif token=='tabdoctopics':
                    newstring = tables.doctopics(uri)
                elif token=='tabdocerrors':
                    newstring = tables.docerrors(uri)
                elif token=='tabfile_reports':
                    newstring = tables.filereports(uri)
                elif token=='tabfile_report':
                    newstring = tables.filereport(uri)
                elif token=='tabdocfileerrors':
                    newstring = tables.docfileerrors(uri)
                elif token=='tabdocnotes':
                    newstring = tables.docnotes(uri)
                elif token=='tabcvslog':
                    newstring = tables.cvslog(uri)
                elif token=='tabletters':
                    newstring = tables.letters(uri)
                elif token=='tabusers':
                    newstring = tables.users(uri)
                elif token=='tabuser':
                    newstring = tables.user(uri)
                elif token=='tabrecentnews':
                    newstring = tables.recent_news(uri)
                elif token=='tabsubtopic':
                    newstring = tables.subtopic(uri)
                elif token=='tabtypedocs':
                    newstring = tables.doctable(uri, type_code=uri.code, lang=uri.lang)
                elif token=='tabsubtopicdocs':
                    newstring = tables.doctable(uri, subtopic_code=uri.code, lang=uri.lang)
                elif token=='tabsitemap':
                    newstring = tables.sitemap(uri)
                elif token=='tabsessions':
                    newstring = tables.tabsessions(uri)
                elif token=='tabmailpass':
                    newstring = tables.tabmailpass(uri)
                elif token=='taberrors':
                    newstring = tables.errors(uri)
                elif token=='tabsearch':
                    newstring = tables.tabsearch(uri)
                elif token=='tabsplashlanguages':
                    newstring = tables.tabsplashlanguages(uri)
            
                # Blocks and Strings
                if newstring==None:
                    block = lampadasweb.blocks[token]
                    if block==None:
                        string = lampadasweb.strings[token]
                        if string==None:
                            log(1, 'Could not replace token ' + token)
                        else:
                            newstring = string.string[uri.lang]
                    else:
                        newstring = block.block
                
                # Add an error message if the token was not found
                if newstring==None:
                    log(1, 'Could not replace token ' + token)
                    newstring = 'ERROR (' + token + ')'
                
                # Call myself recursively before replacing, so we do replacement on it only once,
                # while it is still small. Replacing text in large pages is more costly on large
                # strings.
                # 
                # Routines that build potentially very large tables should be caching their
                # static portions during page build.
                temp = temp.replace(temp[pos:pos2+1], self.replace_tokens(page, uri, newstring))
                
                temp = temp.replace('\|', 'DCM_PIPE')
                pos = temp.find('|')
        
        return temp
        

page_factory = PageFactory()

def benchmark(url, reps):
    from DataLayer import Lampadas
    for x in range(0, reps):
        page = page_factory.page(url)

def main():
    import profile
    import pstats

    if len(sys.argv[1:]):
        profile_it = 0
        reps_flag = 0
        profile_reps = 100
        for arg in sys.argv[1:]:
            if reps_flag:
                profile_reps = int(arg)
                reps_flag = 0
            elif arg=='-p' or arg=='--profile':
                profile_it = 1
            elif arg=='-r' or arg=='--reps':
                reps_flag = 1
            elif profile_it > 0:
                print 'Profiling, ' + str(profile_reps) + ' repetitions...'
                page = page_factory.page(arg)
                profile.run('benchmark("' + arg + '", ' + str(profile_reps) + ')', 'profile_stats')
                p = pstats.Stats('profile_stats')
                p.sort_stats('time').print_stats()

            else:
                print page_factory.page(URI(arg))
    else:
        profile()


if __name__=="__main__":
    main()

