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
        combo = "<select name='class'>\n"
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
            if doc.LanguageCode == lang or lang == None:
                combo = combo + "<option "
                if doc.ID == value:
                    combo = combo + "selected "
                combo = combo + "value='" + str(doc.ID) + "'>"
                combo = combo + doc.Title
                combo = combo + "</option>\n"
        combo = combo + "</select>"
        return combo

    def DTD(self, value, lang):
        self.combo = "<select name='dtd'>\n"
        keys = lampadas.DTDs.keys()
        for key in keys:
            dtd = lampadas.DTDs[key]
            assert not dtd == None
            self.combo = self.combo + "<option "
            if dtd.DTD == value:
                self.combo = self.combo + "selected "
            self.combo = self.combo + "value='" + dtd.DTD + "'>"
            self.combo = self.combo + dtd.DTD
            self.combo = self.combo + "</option>\n"
        self.combo = self.combo + "</select>"
        return self.combo
    
    def Format(self, value, lang):
        self.combo = "<select name='format'>\n"
        keys = lampadas.Formats.keys()
        for key in keys:
            format = lampadas.Formats[key]
            assert not format == None
            self.combo = self.combo + "<option "
            if format.ID == value:
                self.combo = self.combo + "selected "
            self.combo = self.combo + "value='" + str(format.ID) + "'>"
            self.combo = self.combo + format.i18n[lang].Name
            self.combo = self.combo + "</option>\n"
        self.combo = self.combo + "</select>"
        return self.combo

    def Language(self, value, lang):
        return "lang"

    def License(self, value, lang):
        return "license"

    def PubStatus(self, value, lang):
        self.combo = "<select name='pub_status'>\n"
        keys = lampadas.PubStatuses.keys()
        for key in keys:
            PubStatus = lampadas.PubStatuses[key]
            assert not PubStatus == None
            self.combo = self.combo + "<option "
            if PubStatus.Code == value:
                self.combo = self.combo + "selected "
            self.combo = self.combo + "value='" + str(PubStatus.Code) + "'>"
            self.combo = self.combo + PubStatus.I18n[lang].Name
            self.combo = self.combo + "</option>\n"
        self.combo = self.combo + "</select>"
        return self.combo
        
    def ReviewStatus(self, value, lang):
        self.combo = "<select name='review_status'>\n"
        keys = lampadas.ReviewStatuses.keys()
        for key in keys:
            ReviewStatus = lampadas.ReviewStatuses[key]
            assert not ReviewStatus == None
            self.combo = self.combo + "<option "
            if ReviewStatus.Code == value:
                self.combo = self.combo + "selected "
            self.combo = self.combo + "value='" + str(ReviewStatus.Code) + "'>"
            self.combo = self.combo + ReviewStatus.I18n[lang].Name
            self.combo = self.combo + "</option>\n"
        self.combo = self.combo + "</select>"
        return self.combo


# BoxFactory

class BoxFactory:

    def main_menu(self, lang):
        self.box = ''
        self.box = self.box + '<table class="navbox"><tr><th>|mmtitle|</th></tr>'
        self.box = self.box + '<tr><td>'
        self.box = self.box + '<a href="home">|home|</a><br>'
        self.box = self.box + '<a href="doctable">|doctable|</a><br>'
        self.box = self.box + '<a href="downloads">Downloads</a>'
        self.box = self.box + '</td></tr>'
        self.box = self.box + '</table>'
        return self.box


class TableFactory:

    combof = ComboFactory()

    def bar_graph(self, value, max, lang):
        return str(value) + '/' + str(max)

    def doc(self, DocID, lang):
        self.box = ''
        self.box = self.box + '<table class="box" style="width:100%"><tr><th colspan="6">|docdetails|</th></tr>'
        if DocID:
            doc = lampadas.Docs[DocID]
            self.box = self.box + '<form method=POST action="docsave" name="document">'
        else:
            doc = Doc()
            self.box = self.box + '<form method=POST action="docadd" name="document">'
            
        self.box = self.box + '<input name="doc_id" type=hidden value=' + str(doc.ID) + '>\n'
        self.box = self.box + '<tr>\n'
        self.box = self.box + '<th align=right>Title</th><td colspan=5><input type=text name=title size=60 style="width:100%" value="' + doc.Title + '"></td>\n'
        self.box = self.box + '</tr>\n'
        self.box = self.box + '<tr>\n'
        self.box = self.box + '<th align=right>'
        if doc.URL:
            self.box = self.box + '<a href="' + doc.URL + '">URL</a>'
        else:
            self.box = self.box + 'URL'
        self.box = self.box + '</th><td colspan=5><input type=text name=url size=60 style="width:100%" value="' + doc.URL + '"></td>'
        self.box = self.box + '</tr>\n<tr>\n'
        self.box = self.box + '<th align=right>'

        if doc.HomeURL:
            self.box = self.box + '<a href="' + doc.HomeURL + '">Home URL</a>'
        else:
            self.box = self.box + 'Home URL'
        self.box = self.box + '</th><td colspan=5><input type=text name=ref_url size=60 style="width:100%" value="' + doc.HomeURL + '"></td>'
        self.box = self.box + '</tr>\n<tr>\n'
        self.box = self.box + '<th align=right>Status</th><td>'
        self.box = self.box + self.combof.PubStatus(doc.PubStatusCode, lang)
        self.box = self.box + '</td>'
        self.box = self.box + '<th align=right>Class</th><td>\n'
        self.box = self.box + self.combof.Class(doc.ClassID, lang)
        self.box = self.box + '</td>'
        self.box = self.box + '<th align=right>Maint</th><td>\n'
        if doc.Maintained:
            self.box = self.box + "Yes"
        else:
            self.box = self.box + "No"
        self.box = self.box + '</td>'
        self.box = self.box + '</tr>\n<tr>\n'
        self.box = self.box + '<th align=right>Language</th><td>'
        self.box = self.box + self.combof.ReviewStatus(doc.ReviewStatus, lang)
        self.box = self.box + '</td>'
        self.box = self.box + '<th align=right>Accuracy</th><td>'
        self.box = self.box + self.combof.ReviewStatus(doc.TechReviewStatus, lang)
        self.box = self.box + '</td>'
        self.box = self.box + '<th align=right>License</th><td>'
        self.box = self.box + self.combof.License(doc.License, lang)
        self.box = self.box + '</td>'
        self.box = self.box + '</tr>\n<tr>\n'
        self.box = self.box + '<th align=right>Pub Date</th><td><input type=text name=pub_date size=10 value="' + doc.PubDate + '"></td>'
        self.box = self.box + '<th align=right>Updated</th><td><input type=text name=last_update size=10 value="' + doc.LastUpdate + '"></td>'
        self.box = self.box + '<th align=right>Version</th><td><input type=text name=version size=10 value="' + doc.Version + '"></td>'
        self.box = self.box + '</tr>\n<tr>\n'
        self.box = self.box + '<th align=right>Tickle Date</th><td><input type=text name=tickle_date size=10 value="' + doc.TickleDate + '"></td>'
        self.box = self.box + '<th align=right>ISBN</th><td><input type=text name=isbn size=14 value="' + doc.ISBN + '"></td>'
        self.box = self.box + '<th align=right>Rating</th>\n'
        self.box = self.box + '<td>'
        self.box = self.box + self.bar_graph(doc.Rating, 10, lang)
        self.box = self.box + '</td>\n'
        if DocID:
            self.box = self.box + '</tr>\n<tr>\n'
            self.box = self.box + '<th align=right>Format</th><td>'
            self.box = self.box + lampadas.Formats[doc.FormatID].I18n[lang].Name
            self.box = self.box + '</td>'
            self.box = self.box + '<th align=right>DTD</th><td>'
            self.box = self.box + doc.DTD + ' ' + doc.DTDVersion
            self.box = self.box + '</td>'
            self.box = self.box + '<th align=right>Lang</th><td>'
            self.box = self.box + self.combof.Language(doc.Lang, lang)
            self.box = self.box + '</td>'
        self.box = self.box + '</tr>\n<tr>\n'
        self.box = self.box + '<th align=right>Abstract</th>'
        self.box = self.box + '<td colspan=5><textarea name=abstract rows=6 cols=40 style="width:100%" wrap>' + doc.Abstract + '</textarea></td>\n'
        self.box = self.box + '</tr>\n'
        self.box = self.box + '<tr><td></td><td><input type=submit name=save value=Save></td></tr>\n'
        self.box = self.box + '</form>\n'
        self.box = self.box + '</table>\n'

        return self.box

    def docs(self, lang):
        self.box = ''
        self.box = self.box + '<table class="box"><tr><th colspan="2">Title</th></tr>'
        keys = lampadas.Docs.keys()
        for key in keys:
            if lampadas.Docs[key].Lang == lang:
                self.box = self.box + '<tr>'
                self.box = self.box + '<td><a href="/editdoc/' + str(lampadas.Docs[key].ID) + '/">' + EDIT_ICON + '</a></td>'
                self.box = self.box + '<td><a href="/doc/' + str(lampadas.Docs[key].ID) + '/">' + lampadas.Docs[key].Title + '</a></td>'
                self.box = self.box + '</tr>'
        self.box = self.box + '</table>'
        return self.box


# PageFactory

class PageFactory:

    boxf    = BoxFactory()
    tablef  = TableFactory()

    def __call__(self, key, lang):
        return self.page(key, lang)

    def page(self, key):
        uri = URI(key)
        uri.printdebug()
        log(3, 'Serving language ' + uri.language)
        
        if uri.service == 'doc':
            if uri.format == '':
                html = self.doc_page(uri)
        else:
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

                # Boxes
                # 
                if token=='boxmainmenu':
                    newstring = self.boxf.main_menu(uri.language)
            
                # Tables
                # 
                if token=='tabdocstable':
                    newstring = self.tablef.docs(uri.language)
            
                if token=='tabeditdoc':
                    newstring = self.tablef.doc(uri.id, uri.language)
            
                # Blocks and Strings
                # 
                if newstring == '':
                    block = lampadasweb.blocks[token]
                    if block == None:
                        string = lampadasweb.strings[token]
                        if string == None:
                            newstring = 'ERROR'
                            log(1, 'Could not replace token ' + token)
                        else:
                            newstring = string.i18n[uri.language].string
                    else:
                        newstring = block.i18n[uri.language].block
                
                if newstring == '':
                    log(1, 'Could not replace token ' + token)
                else:
                    html = html.replace(html[pos:pos2+1], newstring)
                    html = html.replace('\|', 'DCM_PIPE')
                
                pos = html.find('|')
        
        html = html.replace('DCM_PIPE', '|')
    
        log(3, 'Page built ' + page.code)
        return html

    def doc_page(self, uri):
        lang  = uri.language
        doc = lampadas.Docs[uri.id]
        if doc == None:
            html = "Error, could not locate document " + str(uri.id)
        else:
            cachedir = config.cache_dir + str(uri.id) + '/'
            
            files = doc.Files
            if files.Count() == 0:
                html = 'No file to process'
            elif files.Count() > 1:
                html = 'Only single files supported right now'
            else:
                command = 'cd ' + cachedir + '; make index'
                os.system(command)
                
                if uri.filename == '':
                    uri.filename = 'index.html'
                
                if os.access(cachedir + uri.filename, os.F_OK):
                    fh = open(cachedir + uri.filename)
                    html = fh.read()
                    fh.close()
                else:
                    html = 'Document cannot be found'
        return html


page_factory = PageFactory()

def main():
    for arg in sys.argv[1:]:
        print page_factory.page(arg)


def usage():
    print "HTMlampadas.py version " + VERSION


if __name__ == "__main__":
    main()
