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
from DataLayer import lampadas
from WebLayer import lampadasweb

import commands
from string import split
import sys
import os


# Globals


# Constants

EDIT_ICON = '<img src="images/edit.png" alt="Edit" height="20" width="20" border="0" hspace="5" vspace="0" align="top">'


# ComboFactory

class ComboFactory:

    def Class(self, value, lang):
        combo = "<select name='class_id'>\n"
        keys = lampadas.Classes.keys()
        for key in keys:
            classfoo = lampadas.Classes[key]
            assert not classfoo == None
            combo = combo + "<option "
            if classfoo.ID == value:
                combo = combo + "selected "
            combo = combo + "value='" + str(classfoo.ID) + "'>"
            combo = combo + classfoo.I18n[lang].Name
            combo = combo + "</option>\n"
        combo = combo + "</select>"
        return combo

    def Doc(self, value, lang):
        combo = "<select name='doc'>\n"
        keys = lampadas.Docs.keys()
        for key in keys:
            doc = lampadas.Docs[key]
            assert not doc == None
            if doc.Lang == lang or lang == None:
                combo = combo + "<option "
                if doc.ID == value:
                    combo = combo + "selected "
                combo = combo + "value='" + str(doc.ID) + "'>"
                combo = combo + doc.Title
                combo = combo + "</option>\n"
        combo = combo + "</select>"
        return combo

    def DTD(self, value, lang):
        combo = "<select name='dtd'>\n"
        keys = lampadas.DTDs.keys()
        for key in keys:
            dtd = lampadas.DTDs[key]
            assert not dtd == None
            combo = combo + "<option "
            if dtd.DTD == value:
                combo = combo + "selected "
            combo = combo + "value='" + dtd.DTD + "'>"
            combo = combo + dtd.DTD
            combo = combo + "</option>\n"
        combo = combo + "</select>"
        return combo
    
    def Format(self, value, lang):
        combo = "<select name='format'>\n"
        keys = lampadas.Formats.keys()
        for key in keys:
            format = lampadas.Formats[key]
            assert not format == None
            combo = combo + "<option "
            if format.ID == value:
                combo = combo + "selected "
            combo = combo + "value='" + str(format.ID) + "'>"
            combo = combo + format.i18n[lang].Name
            combo = combo + "</option>\n"
        combo = combo + "</select>"
        return combo

    def Language(self, value, lang):
        combo = "<select name='lang'>\n"
        keys = lampadas.Languages.keys()
        for key in keys:
            language = lampadas.Languages[key]
            assert not language == None
            combo = combo + "<option "
            if language.Code == value:
                combo = combo + "selected "
            combo = combo + "value='" + language.Code + "'>"
            combo = combo + language.I18n[lang].Name
            combo = combo + "</option>\n"
        combo = combo + "</select>"
        return combo

    def License(self, value, lang):
        combo = "<select name='license'>\n"
        keys = lampadas.Licenses.keys()
        for key in keys:
            license = lampadas.Licenses[key]
            assert not license == None
            combo = combo + "<option "
            if license.License == value:
                combo = combo + "selected "
            combo = combo + "value='" + str(license.License) + "'>"
            combo = combo + license.License
            combo = combo + "</option>\n"
        combo = combo + "</select>"
        return combo

    def Page(self, value, lang):
        combo = "<select name='page_code'>\n"
        keys = lampadasweb.pages.keys()
        for key in keys:
            page = lampadasweb.pages[key]
            assert not page == None
            combo = combo + "<option "
            if Page.Code == value:
                combo = combo + "selected "
            combo = combo + "value='" + str(page.Code) + "'>"
            combo = combo + page.I18n[lang].Title
            combo = combo + "</option>\n"
        combo = combo + "</select>"
        return combo

    def PubStatus(self, value, lang):
        combo = "<select name='pub_status_code'>\n"
        keys = lampadas.PubStatuses.keys()
        for key in keys:
            PubStatus = lampadas.PubStatuses[key]
            assert not PubStatus == None
            combo = combo + "<option "
            if PubStatus.Code == value:
                combo = combo + "selected "
            combo = combo + "value='" + str(PubStatus.Code) + "'>"
            combo = combo + PubStatus.I18n[lang].Name
            combo = combo + "</option>\n"
        combo = combo + "</select>"
        return combo
        
    def ReviewStatus(self, value, lang):
        combo = "<select name='review_status_code'>\n"
        keys = lampadas.ReviewStatuses.keys()
        for key in keys:
            ReviewStatus = lampadas.ReviewStatuses[key]
            assert not ReviewStatus == None
            combo = combo + "<option "
            if ReviewStatus.Code == value:
                combo = combo + "selected "
            combo = combo + "value='" + str(ReviewStatus.Code) + "'>"
            combo = combo + ReviewStatus.I18n[lang].Name
            combo = combo + "</option>\n"
        combo = combo + "</select>"
        return combo

    def TechReviewStatus(self, value, lang):
        combo = "<select name='tech_review_status_code'>\n"
        keys = lampadas.ReviewStatuses.keys()
        for key in keys:
            ReviewStatus = lampadas.ReviewStatuses[key]
            assert not ReviewStatus == None
            combo = combo + "<option "
            if ReviewStatus.Code == value:
                combo = combo + "selected "
            combo = combo + "value='" + str(ReviewStatus.Code) + "'>"
            combo = combo + ReviewStatus.I18n[lang].Name
            combo = combo + "</option>\n"
        combo = combo + "</select>"
        return combo

    def Subtopic(self, value, lang):
        combo = '<select name="subtopic_code">\n'
        keys = lampadas.Subtopics.sort_by('sort_order')
        for key in keys:
            subtopic = lampadas.subtopics[key]
            assert not subtopic == None
            combo = combo + "<option "
            if subtopic.code == value:
                combo = combo + "selected "
            combo = combo + "value='" + str(subtopic.code) + "'>"
            combo = combo + subtopic.i18n[lang].name
            combo = combo + "</option>\n"
        combo = combo + "</select>"
        return combo


# BoxFactory

class BoxFactory:

    def section_menu(self, section_code, lang):
        log(3, "Creating section menu: " + section_code)
        section = lampadasweb.sections[section_code]
        assert not section == None
        box = '<table class="navbox"><tr><th>' + section.i18n[lang].name + '</th></tr>\n'
        box = box + '<tr><td>'
        keys = lampadasweb.pages.sort_by('sort_order')
        for key in keys:
            page = lampadasweb.pages[key]
            if page.section_code == section_code:
                log(3, 'adding item: ' + page.code + ', citeref: ' + page.i18n[lang].menu_name)
                box = box + '<a href="' + page.code + '">' + page.i18n[lang].menu_name + '</a><br>\n'
        box = box + '</td></tr></table>\n'
        log(3, "section menu complete")
        return box


class TableFactory:

    combof = ComboFactory()
    boxf = BoxFactory()

    def bar_graph(self, value, max, lang):
        return str(value) + '/' + str(max)

    def doc(self, DocID, lang):
        box = ''
        box = box + '<table class="box" style="width:100%"><tr><th colspan="6">|docdetails|</th></tr>'
        if DocID:
            doc = lampadas.Docs[DocID]
            box = box + '<form method=POST action="data/save/document" name="document">'
        else:
            doc = Doc()
            box = box + '<form method=POST action="data/save/newdocument" name="document">'
            
        box = box + '<input name="doc_id" type=hidden value=' + str(doc.ID) + '>\n'
        box = box + '<tr>\n'
        box = box + '<th align=right>Title</th><td colspan=5><input type=text name=title size=60 style="width:100%" value="' + doc.Title + '"></td>\n'
        box = box + '</tr>\n'
        box = box + '<tr>\n'
        box = box + '<th align=right>'
        if doc.URL:
            box = box + '<a href="' + doc.URL + '">URL</a>'
        else:
            box = box + 'URL'
        box = box + '</th><td colspan=5><input type=text name=url size=60 style="width:100%" value="' + doc.URL + '"></td>'
        box = box + '</tr>\n<tr>\n'
        box = box + '<th align=right>'

        if doc.HomeURL:
            box = box + '<a href="' + doc.HomeURL + '">Home URL</a>'
        else:
            box = box + 'Home URL'
        box = box + '</th><td colspan=5><input type=text name=ref_url size=60 style="width:100%" value="' + doc.HomeURL + '"></td>'
        box = box + '</tr>\n<tr>\n'
        box = box + '<th align=right>Status</th><td>'
        box = box + self.combof.PubStatus(doc.PubStatusCode, lang)
        box = box + '</td>\n'
        box = box + '<th align=right>Class</th><td>\n'
        box = box + self.combof.Class(doc.ClassID, lang)
        box = box + '</td>\n'
        box = box + '<th align=right>Maint</th><td>\n'
        if doc.Maintained:
            box = box + "Yes"
        else:
            box = box + "No"
        box = box + '</td>'
        box = box + '</tr>\n<tr>\n'
        box = box + '<th align=right>Writing</th><td>'
        box = box + self.combof.ReviewStatus(doc.ReviewStatusCode, lang)
        box = box + '</td>\n'
        box = box + '<th align=right>Accuracy</th><td>'
        box = box + self.combof.TechReviewStatus(doc.TechReviewStatusCode, lang)
        box = box + '</td>\n'
        box = box + '<th align=right>License</th><td>'
        box = box + self.combof.License(doc.License, lang)
        box = box + '</td>'
        box = box + '</tr>\n<tr>\n'
        box = box + '<th align=right>Pub Date</th><td><input type=text name=pub_date size=10 value="' + doc.PubDate + '"></td>'
        box = box + '<th align=right>Updated</th><td><input type=text name=last_update size=10 value="' + doc.LastUpdate + '"></td>'
        box = box + '<th align=right>Version</th><td><input type=text name=version size=10 value="' + doc.Version + '"></td>'
        box = box + '</tr>\n<tr>\n'
        box = box + '<th align=right>Tickle Date</th><td><input type=text name=tickle_date size=10 value="' + doc.TickleDate + '"></td>'
        box = box + '<th align=right>ISBN</th><td><input type=text name=isbn size=14 value="' + doc.ISBN + '"></td>'
        box = box + '<th align=right>Rating</th>\n'
        box = box + '<td>'
        box = box + self.bar_graph(doc.Rating, 10, lang)
        box = box + '</td>\n'
        box = box + '</tr>\n<tr>\n'
        box = box + '<th align=right>Format</th><td>'
        box = box + lampadas.Formats[doc.FormatID].I18n[lang].Name
        box = box + '</td>'
        box = box + '<th align=right>DTD</th><td>'
        box = box + doc.DTD + ' ' + doc.DTDVersion
        box = box + '</td>'
        box = box + '<th align=right>Lang</th><td>'
        box = box + self.combof.Language(doc.Lang, lang)
        box = box + '</td>'
        box = box + '</tr>\n<tr>\n'
        box = box + '<th align=right>Abstract</th>'
        box = box + '<td colspan=5><textarea name=abstract rows=6 cols=40 style="width:100%" wrap>' + doc.Abstract + '</textarea></td>\n'
        box = box + '</tr>\n'
        box = box + '<tr><td></td><td><input type=submit name=save value=Save></td></tr>\n'
        box = box + '</form>\n'
        box = box + '</table>\n'

        return box

    def doctable(self, lang):
        log(3, "Creating doctable")
        box = ''
        box = box + '<table class="box"><tr><th colspan="2">|title|</th></tr>'
        keys = lampadas.Docs.sort_by("Title")
        for key in keys:
            doc = lampadas.Docs[key]
            if doc.Lang == lang:
                box = box + '<tr>'
                box = box + '<td><a href="editdoc/' + str(doc.ID) + '/">' + EDIT_ICON + '</a></td>'
                box = box + '<td><a href="doc/' + str(doc.ID) + '/">' + doc.Title + '</a></td>'
                box = box + '</tr>\n'
        box = box + '</table>'
        log(3, "doctable complete")
        return box

    def menus(self, lang):
        log(3, "Creating all section menus")
        box = ''
        keys = lampadasweb.sections.sort_by('sort_order')
        for key in keys:
            box = box + self.boxf.section_menu(key, lang)
        log(3, "all section menus complete")
        return box

    def recent_news(self, lang):
        log(3, 'Creating recent news')
        box = '<table class="box"><tr><th>|date|</th><th>|news|</th></tr>\n'
        keys = lampadasweb.news.sort_by_desc('pub_date')
        for key in keys:
            news = lampadasweb.news[key]
            if not news.i18n[lang] == None:
                box = box + '<tr>\n'
                box = box + '<td>' + news.pub_date + '</td>\n'
                box = box + '<td>' + news.i18n[lang].news + '</td>\n'
                box = box + '</tr>\n'
        box = box + '</table>\n'
        log(3, 'Recent news table complete')
        return box

    def topics(self, lang):
        log(3, 'Creating topics table')
        box = '<table class="navbox"><tr><th>|topics|</th></tr>\n'
        box = box + '<tr><td><ol>\n'
        keys = lampadas.topics.sort_by('num')
        for key in keys:
            topic = lampadas.topics[key]
            box = box + '<li><a href="topic/' + topic.code + '">\n'
            box = box + topic.i18n[lang].name + '</a>\n'
        box = box + '</ol></td></tr>\n'
        box = box + '</table>\n'
        log(3, "Topics table complete")
        return box

    def subtopics(self, topic_code, lang):
        log(3, 'Creating subtopics table')
        topic = lampadas.topics[topic_code]
        box = '<table class="navbox"><tr><th>' + topic.i18n[lang].name + '</th></tr>\n'
        box = box + '<tr><td><ol>\n'
        keys = lampadas.subtopics.sort_by('num')
        for key in keys:
            subtopic = lampadas.subtopics[key]
            if subtopic.topic_code == topic_code:
                box = box + '<li><a href="subtopic/' + subtopic.code + '">\n'
                box = box + subtopic.i18n[lang].name + '</a>\n'
        box = box + '</ol></td></tr>\n'
        box = box + '</table>\n'
        log(3, "Topics table complete")
        return box

    def classes(self, lang):
        log(3, 'Creating classes table')
        box = '<table class="navbox"><tr><th>|classes|</th></tr>\n'
        box = box + '<tr><td>\n'
        keys = lampadas.Classes.sort_by('sort_order')
        for key in keys:
            Class = lampadas.Classes[key]
            box = box + '<a href="class/' + str(Class.ID) + '">\n'
            box = box + Class.I18n[lang].Name + '</a><br>\n'
        box = box + '</td></tr>\n'
        box = box + '</table>\n'
        log(3, "Classes table complete")
        return box


# PageFactory

class PageFactory:

    boxf    = BoxFactory()
    tablef  = TableFactory()

    def __call__(self, key, lang):
        return self.page(key, lang)

    def page_exists(self, key):
        uri = URI(key)
        if uri.path == '' and lampadasweb.pages[uri.filename]:
            return 1
        return

    def page(self, key):
        uri = URI(key)
        log(3, 'Serving language ' + uri.language)
        
        page = lampadasweb.pages[uri.filename]
        if page == None:
            page = lampadasweb.pages['404']
        assert not page == None
        html = self.build_page(page, uri)

        return html
    

    def build_page(self, page, uri):
        template = lampadasweb.templates[page.template_code]
        assert not template == None
        html = template.template

        html = html.replace('\|', 'DCM_PIPE')
    
        pos = html.find('|')
        while pos <> -1 :
            pos2 = html.find('|', pos+1)
            if pos2 == -1:
                pos = -1
            else:
                oldstring = html[pos:pos2+1]
                token = html[pos+1:pos2]
            
                newstring = ''
            
                # Built-ins
                # 
                if token=='title':
                    newstring = page.i18n[uri.language].title
                if token=='body':
                    newstring = page.i18n[uri.language].page
                if token=='hostname':
                    newstring = config.hostname
                if token=='rootdir':
                    newstring = config.root_dir
                if token=='port':
                    newstring = str(config.port)
                if token=='base':
                    newstring = 'http://' + config.hostname + ':' + str(config.port) + config.root_dir
                    if uri.force_lang:
                        newstring = newstring + uri.language + '/'
                if token=='page':
                    newstring = page.code
                if token=='stylesheet':
                    newstring='default'
                if token=='version':
                    newstring = VERSION

                # Tables
                # 
                if token=='tabdocs':
                    newstring = self.tablef.doctable(uri.language)
                if token=='tabeditdoc':
                    newstring = self.tablef.doc(uri.id, uri.language)
                if token=='tabmenus':
                    newstring = self.tablef.menus(uri.language)
                if token=='tabrecentnews':
                    newstring = self.tablef.recent_news(uri.language)
                if token=='tabtopics':
                    newstring = self.tablef.topics(uri.language)
                if token=='tabsubtopics':
                    newstring = self.tablef.subtopics(uri.code, uri.language)
                if token=='tabclasses':
                    newstring = self.tablef.classes(uri.language)
            
                # Blocks and Strings
                # 
                if newstring == '':
                    block = lampadasweb.blocks[token]
                    if block == None:
                        string = lampadasweb.strings[token]
                        if string == None:
                            log(1, 'Could not replace token ' + token)
                        else:
                            newstring = string.i18n[uri.language].string
                    else:
                        newstring = block.i18n[uri.language].block
                
                # Add an error message if the token was not found
                # 
                if newstring == '':
                    log(1, 'Could not replace token ' + token)
                    newstring = 'ERROR (' + token + ')'
                
                html = html.replace(html[pos:pos2+1], newstring)
                html = html.replace('\|', 'DCM_PIPE')
                
                pos = html.find('|')
        
        html = html.replace('DCM_PIPE', '|')
    
        log(3, 'Page built ' + page.code)
        return html


page_factory = PageFactory()

def profile():
    import profile

    profile.run('page_factory.page("home")')
    
def main():
    if len(sys.argv[1:]):
        for arg in sys.argv[1:]:
            print page_factory.page(arg)
    else:
        profile()


if __name__ == "__main__":
    main()
