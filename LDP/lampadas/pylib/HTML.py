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
from Weblayer import lampadasweb

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
            self.combo = self.combo + format.I18n[lang].Name
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

    def MainMenu(self, lang):
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

    Combo = ComboFactory()

    def BarGraph(self, value, max, lang):
        return str(value) + '/' + str(max)

    def Doc(self, DocID, lang):
        self.box = ''
        self.box = self.box + '<table class="box" style="width:100%"><tr><th colspan="6">|docdetails|</th></tr>'
        if DocID:
            Doc = lampadas.Docs[DocID]
            self.box = self.box + '<form method=POST action="docsave" name="document">'
        else:
            Doc = Doc()
            self.box = self.box + '<form method=POST action="docadd" name="document">'
            
        self.box = self.box + '<input name="doc_id" type=hidden value=' + str(Doc.ID) + '>\n'
        self.box = self.box + '<tr>\n'
        self.box = self.box + '<th align=right>Title</th><td colspan=5><input type=text name=title size=60 style="width:100%" value="' + Doc.Title + '"></td>\n'
        self.box = self.box + '</tr>\n'
        self.box = self.box + '<tr>\n'
        self.box = self.box + '<th align=right>'
        if Doc.URL:
            self.box = self.box + '<a href="' + Doc.URL + '">URL</a>'
        else:
            self.box = self.box + 'URL'
        self.box = self.box + '</th><td colspan=5><input type=text name=url size=60 style="width:100%" value="' + Doc.URL + '"></td>'
        self.box = self.box + '</tr>\n<tr>\n'
        self.box = self.box + '<th align=right>'

        if Doc.HomeURL:
            self.box = self.box + '<a href="' + Doc.HomeURL + '">Home URL</a>'
        else:
            self.box = self.box + 'Home URL'
        self.box = self.box + '</th><td colspan=5><input type=text name=ref_url size=60 style="width:100%" value="' + Doc.HomeURL + '"></td>'
        self.box = self.box + '</tr>\n<tr>\n'
        self.box = self.box + '<th align=right>Status</th><td>'
        self.box = self.box + self.Combo.PubStatus(Doc.PubStatusCode, lang)
        self.box = self.box + '</td>'
        self.box = self.box + '<th align=right>Class</th><td>\n'
        self.box = self.box + self.Combo.Class(Doc.ClassID, lang)
        self.box = self.box + '</td>'
        self.box = self.box + '<th align=right>Maint</th><td>\n'
        if Doc.Maintained:
            self.box = self.box + "Yes"
        else:
            self.box = self.box + "No"
        self.box = self.box + '</td>'
        self.box = self.box + '</tr>\n<tr>\n'
        self.box = self.box + '<th align=right>Language</th><td>'
        self.box = self.box + self.Combo.ReviewStatus(Doc.ReviewStatus, lang)
        self.box = self.box + '</td>'
        self.box = self.box + '<th align=right>Accuracy</th><td>'
        self.box = self.box + self.Combo.ReviewStatus(Doc.TechReviewStatus, lang)
        self.box = self.box + '</td>'
        self.box = self.box + '<th align=right>License</th><td>'
        self.box = self.box + self.Combo.License(Doc.License, lang)
        self.box = self.box + '</td>'
        self.box = self.box + '</tr>\n<tr>\n'
        self.box = self.box + '<th align=right>Pub Date</th><td><input type=text name=pub_date size=10 value="' + Doc.PubDate + '"></td>'
        self.box = self.box + '<th align=right>Updated</th><td><input type=text name=last_update size=10 value="' + Doc.LastUpdate + '"></td>'
        self.box = self.box + '<th align=right>Version</th><td><input type=text name=version size=10 value="' + Doc.Version + '"></td>'
        self.box = self.box + '</tr>\n<tr>\n'
        self.box = self.box + '<th align=right>Tickle Date</th><td><input type=text name=tickle_date size=10 value="' + Doc.TickleDate + '"></td>'
        self.box = self.box + '<th align=right>ISBN</th><td><input type=text name=isbn size=14 value="' + Doc.ISBN + '"></td>'
        self.box = self.box + '<th align=right>Rating</th>\n'
        self.box = self.box + '<td>'
        self.box = self.box + self.BarGraph(Doc.Rating, 10, lang)
        self.box = self.box + '</td>\n'
        if DocID:
            self.box = self.box + '</tr>\n<tr>\n'
            self.box = self.box + '<th align=right>Format</th><td>'
            self.box = self.box + lampadas.Formats[Doc.FormatID].I18n[lang].Name
            self.box = self.box + '</td>'
            self.box = self.box + '<th align=right>DTD</th><td>'
            self.box = self.box + Doc.DTD + ' ' + Doc.DTDVersion
            self.box = self.box + '</td>'
            self.box = self.box + '<th align=right>Lang</th><td>'
            self.box = self.box + self.Combo.Language(Doc.Lang, lang)
            self.box = self.box + '</td>'
        self.box = self.box + '</tr>\n<tr>\n'
        self.box = self.box + '<th align=right>Abstract</th>'
        self.box = self.box + '<td colspan=5><textarea name=abstract rows=6 cols=40 style="width:100%" wrap>' + Doc.Abstract + '</textarea></td>\n'
        self.box = self.box + '</tr>\n'
        self.box = self.box + '<tr><td></td><td><input type=submit name=save value=Save></td></tr>\n'
        self.box = self.box + '</form>\n'
        self.box = self.box + '</table>\n'

        return self.box

    def Docs(self, lang):
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
        log.Write(3, 'Serving language ' + uri.Language)
        
        if uri.Service == 'doc':
            if uri.Format == '':
                page = self.DocPage(uri)
        else:
            Page = self.Pages[uri.Filename]
            if Page == None:
                Page = self.Pages['404']
            assert not Page == None
            page = self.build_page(Page, uri)

        return page
    

    def build_page(self, Page, uri):
        Template = self.Templates[Page.TemplateCode]
        assert not Template == None
        page = Template.Template

        page = page.replace('\|', 'DCM_PIPE')
    
        pos = page.find('|')
        while pos <> -1 :
            pos2 = page.find('|', pos+1)
            if pos2 == -1:
                pos = -1
            else:
                oldstring = page[pos:pos2+1]
                token = page[pos+1:pos2]
            
                newstring = ''
            
                # Built-ins
                # 
                if token=='title':
                    newstring = Page.I18n[uri.Language].Title
                if token=='body':
                    newstring = Page.I18n[uri.Language].Page
                if token=='hostname':
                    newstring = config.hostname
                if token=='rootdir':
                    newstring = config.root_dir
                if token=='port':
                    newstring = str(config.pport)
                if token=='base':
                    newstring = 'http://' + config.hostname + ':' + str(config.port) + config.root_dir
                    if uri.ForceLang:
                        newstring = newstring + uri.Language + '/'
                if token=='page':
                    newstring = Page.Code
                if token=='stylesheet':
                    newstring='default'

                # Boxes
                # 
                if token=='boxmainmenu':
                    newstring = self.Box.MainMenu(uri.Language)
            
                # Tables
                # 
                if token=='tabdocstable':
                    newstring = self.Table.Docs(uri.Language)
            
                if token=='tabeditdoc':
                    newstring = self.Table.Doc(uri.ID, uri.Language)
            
                # Blocks and Strings
                # 
                if newstring == '':
                    Block = self.Blocks[token]
                    if Block == None:
                        String = self.Strings[token]
                        if String == None:
                            newstring = 'ERROR'
                            log.Write(1, 'Could not replace token ' + token)
                        else:
                            newstring = String.I18n[uri.Language].String
                    else:
                        newstring = Block.I18n[uri.Language].Block
                
                if newstring == '':
                    log.Write(1, 'Could not replace token ' + token)
                else:
                    page = page.replace(page[pos:pos2+1], newstring)
                    page = page.replace('\|', 'DCM_PIPE')
                
                pos = page.find('|')
        
        page = page.replace('DCM_PIPE', '|')
    
        log.Write(3, 'Page built ' + Page.Code)
        return page

    def DocPage(self, uri):
        DocID = uri.ID
        lang  = uri.Language
        Doc = lampadas.Docs[DocID]
        if Doc == None:
            page = "Error, could not locate document " + str(DocID)
        else:
            cachedir = config.cache_dir + str(Doc.ID) + '/'
            
            Files = Doc.Files
            if Files.Count() == 0:
                page = 'No file to process'
            elif Files.Count() > 1:
                page = 'Only single files supported right now'
            else:
                command = 'cd ' + cachedir + '; make index'
                os.system(command)
                
                if uri.Filename == '':
                    uri.Filename = 'index.html'
                
                if os.access(cachedir + uri.Filename, os.F_OK):
                    fh = open(cachedir + uri.Filename)
                    page = fh.read()
                    fh.close()
                else:
                    page = 'Document cannot be found'
        return page


def main():
    F = PageFactory()
    for arg in sys.argv[1:]:
        print F.Page(arg)


def usage():
    print "HTMlampadas.py version " + VERSION


if __name__ == "__main__":
    main()
