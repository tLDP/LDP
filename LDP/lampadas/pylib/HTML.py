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
from WebLayer import lampadasweb
from Lintadas import lintadas
from Sessions import sessions

import commands
import string
import sys
import os


# Globals


# Constants

EDIT_ICON = '<img src="images/edit.png" alt="Edit" height="20" width="20" '\
            'border="0" hspace="5" vspace="0" align="top">'


# ComboFactory

class ComboFactory:

    def tf(self, name, value, lang):
        log(3, 'creating tf combo: ' + name + ', value is: ' + str(value))
        if value == 1 :
            v1, v2 = 'selected', ''
        else :
            v1, v2 = '', 'selected'
        combo = '<select name="%s">\n' \
                '<option value="1" %s>|stryes|</option>\n' \
                '<option value="0" %s>|strno|</option>\n' \
                '</select>\n' % (name, v1, v2)
        return combo

    def stylesheet(self, value):
        return '<select name="stylesheet">\n</select>\n'
    
    def role(self, value, lang):
        combo = WOStringIO("<select name='role_code'>\n")
        keys = lampadas.roles.sort_by_lang('name', lang)
        for key in keys:
            role = lampadas.roles[key]
            assert not role==None
            combo.write("<option ")
            if role.code==value:
                combo.write("selected ")
            combo.write("value='%s'>%s</option>\n"
                        % (role.code,role.name[lang]))
        combo.write("</select>")
        return combo.get_value()

    def type(self, value, lang):
        combo = WOStringIO("<select name='type_code'>\n" \
                           "<option></option>\n")
        keys = lampadas.types.sort_by('sort_order')
        for key in keys:
            type = lampadas.types[key]
            assert not type==None
            combo.write("<option ")
            if type.code==value:
                combo.write("selected ")
            combo.write("value='%s'>%s</option>\n"
                        % (type.code, type.name[lang]))
        combo.write("</select>")
        return combo.get_value()

    def doc(self, value, lang):
        combo = WOStringIO("<select name='doc'>\n")
        keys = lampadas.docs.sort_by('title')
        for key in keys:
            doc = lampadas.docs[key]
            assert not doc==None
            if doc.lang==lang or lang==None:
                combo.write("<option ")
                if doc.id==value:
                    combo.write("selected ")
                combo.write("value='%s'>%s</option>\n"
                            % (str(doc.id), doc.title))
        combo.write("</select>")
        return combo.get_value()

    def sk_seriesid(self, value, lang):
        combo = WOStringIO('<select name="sk_seriesid">\n')
        combo.write('<option></option>\n')
        keys = lampadas.docs.sort_by('title')
        for key in keys:
            doc = lampadas.docs[key]
            assert not doc==None
            if doc.lang==lang or lang==None:
                combo.write("<option ")
                if doc.sk_seriesid==value:
                    combo.write("selected ")
                if doc.short_title > '':
                    combo.write("value='%s'>%s</option>\n"
                                % (str(doc.sk_seriesid),doc.short_title))
                else:
                    combo.write("value='%s'>%s</option>\n"
                                % (str(doc.sk_seriesid),doc.title[:40]))
        combo.write("</select>\n")
        return combo.get_value()

    def dtd(self, value, lang):
        combo = WOStringIO('<select name="dtd_code">\n' \
                           '<option></option>')
        keys = lampadas.dtds.sort_by('dtd_code')
        for key in keys:
            dtd = lampadas.dtds[key]
            assert not dtd==None
            combo.write("<option ")
            if dtd.dtd_code==value:
                combo.write("selected ")
            combo.write("value='%s'>%s</option>\n"
                        % (dtd.dtd_code,dtd.dtd_code))
        combo.write("</select>\n")
        return combo.get_value()
    
    def format(self, value, lang):
        combo = WOStringIO('<select name="format_code">\n' \
                           '<option></option>')
        keys = lampadas.formats.sort_by_lang('name', lang)
        for key in keys:
            format = lampadas.formats[key]
            assert not format==None
            combo.write("<option ")
            if format.code==value:
                combo.write("selected ")
            combo.write("value='" + str(format.code) + "'>")
            combo.write(format.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def language(self, value, lang):
        combo = WOStringIO("<select name='lang'>\n")
        keys = lampadas.languages.sort_by_lang('name', lang)
        for key in keys:
            language = lampadas.languages[key]
            assert not language==None
            combo.write("<option ")
            if language.code==value:
                combo.write("selected ")
            combo.write("value='" + language.code + "'>")
            combo.write(language.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def license(self, value, lang):
        combo = WOStringIO("<select name='license_code'>\n")
        combo.write('<option></option>')
        keys = lampadas.licenses.sort_by('sort_order')
        for key in keys:
            license = lampadas.licenses[key]
            assert not license==None
            combo.write("<option ")
            if license.license_code==value:
                combo.write("selected ")
            combo.write("value='" + license.license_code + "'>")
            combo.write(license.short_name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def page(self, value, lang):
        combo = WOStringIO("<select name='page_code'>\n")
        keys = lampadasweb.pages.sort_by('page_code')
        for key in keys:
            page = lampadasweb.pages[key]
            assert not page==None
            combo.write("<option ")
            if Page.code==value:
                combo.write("selected ")
            combo.write("value='" + str(page.code) + "'>")
            combo.write(page.title[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def pub_status(self, value, lang):
        combo = WOStringIO("<select name='pub_status_code'>\n")
        combo.write('<option></option>')
        keys = lampadas.pub_statuses.sort_by('sort_order')
        for key in keys:
            PubStatus = lampadas.pub_statuses[key]
            assert not PubStatus==None
            combo.write("<option ")
            if PubStatus.code==value:
                combo.write("selected ")
            combo.write("value='" + str(PubStatus.code) + "'>")
            combo.write(PubStatus.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()
        
    def review_status(self, value, lang):
        combo = WOStringIO("<select name='review_status_code'>\n")
        combo.write('<option></option>')
        keys = lampadas.review_statuses.sort_by('sort_order')
        for key in keys:
            review_status = lampadas.review_statuses[key]
            assert not review_status==None
            combo.write("<option ")
            if review_status.code==value:
                combo.write("selected ")
            combo.write("value='" + str(review_status.code) + "'>")
            combo.write(review_status.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def tech_review_status(self, value, lang):
        combo = WOStringIO("<select name='tech_review_status_code'>\n")
        combo.write('<option></option>')
        keys = lampadas.review_statuses.sort_by('sort_order')
        for key in keys:
            review_status = lampadas.review_statuses[key]
            assert not review_status==None
            combo.write("<option ")
            if review_status.code==value:
                combo.write("selected ")
            combo.write("value='" + str(review_status.code) + "'>")
            combo.write(review_status.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def subtopic(self, value, lang):
        combo = WOStringIO('<select name="subtopic_code">\n')
        topic_codes = lampadas.topics.sort_by('num')
        subtopic_codes = lampadas.subtopics.sort_by('num')
        for topic_code in topic_codes:
            topic = lampadas.topics[topic_code]
            for subtopic_code in subtopic_codes:
                subtopic = lampadas.subtopics[subtopic_code]
                if subtopic.topic_code==topic_code:
                    combo.write("<option ")
                    if subtopic.code==value:
                        combo.write("selected ")
                    combo.write("value='" + str(subtopic.code) + "'>")
                    combo.write(topic.name[lang] + ': ' + subtopic.name[lang])
                    combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

# FIXME -- resume here implementing the use of WOStringIO -- nico

class TableFactory:

    def bar_graph(self, value, max, lang):
        return str(value) + '/' + str(max)

    def doc(self, uri, user):
        if not user:
            return '|blknopermission|'
        elif user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        box = WOStringIO()
        if uri.id > 0:
            lintadas.check(uri.id)
            doc = lampadas.docs[uri.id]
            box.write('<form method=GET action="data/save/document" '\
                      'name="document">')
        else:
            doc = Doc()
            doc.lang = uri.lang
            box.write('<form method=GET action="data/save/newdocument" '\
                      'name="document">')
        box.write('''<input name="username" type="hidden" value="%s">
        <input name="doc_id" type="hidden" value="%s">
        ''' % (user.username, doc.id))
        box.write('''<table class="box" width="100%%">
        <tr><th colspan="6">|strdocdetails|</th></tr>
        <tr><th class="label">|strtitle|</th>
        <td colspan="5">
        <input type="text" name="title" style="width:100%%" value="%s"></td>
        </tr>''' % doc.title)
        box.write('<tr>\n<th class="label">')
        if doc.url:
            box.write('<a href="%s">|strurl|</a>' % doc.url)
        else:
            box.write('|strurl|')
        box.write('</th><td colspan="5"><input type="text" name="url" style="width:100%%" value="%s"></td>' % doc.url)
        box.write('</tr>\n<tr>\n<th class="label">')
        if doc.home_url:
            box.write('<a href="' + doc.home_url + '">|strhome_url|</a>')
        else:
            box.write('|strhome_url|')
        box.write('</th><td colspan="5"><input type="text" name="ref_url" style="width:100%" value="' + doc.home_url + '"></td>')
        box.write('</tr>\n<tr>\n')
        box.write('<th class="label">|strstatus|</th><td>' + combo_factory.pub_status(doc.pub_status_code, uri.lang) + '</td>\n')
        box.write('<th class="label">|strtype|</th><td>' + combo_factory.type(doc.type_code, uri.lang) + '</td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<th class="label">|strversion|</th><td><input type=text name="version" value="' + doc.version + '"></td>\n')
        box.write('<th class="label">|strshort_title|<td><input type=text name="short_title" value="' + doc.short_title + '"></td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<th class="label">|strwriting|</th><td>' + combo_factory.review_status(doc.review_status_code, uri.lang) + '</td>\n')
        box.write('<th class="label">|straccuracy|</th><td>' + combo_factory.tech_review_status(doc.tech_review_status_code, uri.lang) + '</td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<th class="label">|strpub_date|</th><td><input type=text name="pub_date" maxlength="10" value="' + doc.pub_date + '"></td>\n')
        box.write('<th class="label">|strupdated|</th><td><input type=text name="last_update" value="' + doc.last_update + '"></td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<th class="label">|strtickle_date|</th><td><input type=text name="tickle_date" value="' + doc.tickle_date + '"></td>')
        box.write('<th class="label">|strisbn|</th><td><input type=text name="isbn" value="' + doc.isbn + '"></td>')
        box.write('</tr>\n<tr>\n')
        box.write('<th class="label">|strmaintained|</th><td>' + bool2yesno(doc.maintained) + '</td>\n')
        box.write('<th class="label">|strrating|</th><td>' + self.bar_graph(doc.rating, 10, uri.lang) + '</td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<th class="label">|strformat|</th><td>' + combo_factory.format(doc.format_code, uri.lang) + '</td>\n')
        box.write('<th class="label">|strdtd|</th><td>' + combo_factory.dtd(doc.dtd_code, uri.lang))
        box.write(' <input type=text name=dtd_version size=6 value="' + doc.dtd_version + '"></td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<th class="label">|strlanguage|</th><td>' + combo_factory.language(doc.lang, uri.lang) + '</td>\n')
        box.write('<th class="label">|strmaint_wanted|</th><td>' + combo_factory.tf('maintainer_wanted', doc.maintainer_wanted, uri.lang) + '</td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<th class="label">|strlicense|</th><td>' + combo_factory.license(doc.license_code, uri.lang))
        box.write(' <input type=text name=license_version size="6" value="' + doc.license_version + '"></td>\n')
        box.write('<th class="label">|strcopyright_holder|</th><td><input type=text name=copyright_holder value="' + doc.copyright_holder + '"></td>\n')
        box.write('</tr>\n<tr>\n')
        box.write('<th class="label">|strtrans_master|<td colspan="3">' + combo_factory.sk_seriesid(doc.sk_seriesid, uri.lang) + '</td>\n')
        box.write('''
        </tr>
        <tr>
          <th class="label">|strabstract|</th>
          <td colspan="5"><textarea name="abstract" rows="6" cols="40" style="width:100%%" wrap>%s</textarea></td>
        </tr>
        <tr>
          <th class="label">|strshort_desc|</th>
          <td colspan="5"><input type=text name="short_desc" style="width:100%%" value="%s"></td>
        </tr>
        <tr>
          <td></td>
          <td><input type=submit name="save" value="|strsave|"></td>
        </tr>
        </table>
        </form>''' % (doc.abstract, doc.short_desc))
        return box.get_value()

    def docversions(self, uri, user):
        if not user:
            return '|blknopermission|'
        elif user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating docversions table')
        doc = lampadas.docs[uri.id]
        box = '''
        <table class="box" width="100%">
        <tr><th colspan="6">|strdocversions|</th></tr>
        <tr>
        <th class="collabel">|strversion|</th>
        <th class="collabel">|strdate|</th>
        <th class="collabel">|strinitials|</th>
        <th class="collabel">|strcomments|</th> 
        <th class="collabel" colspan="2">|straction|</th> 
        </tr>
        '''
        keys = doc.versions.sort_by('pub_date')
        for key in keys:
            version = doc.versions[key]
            box = box + '<form method=GET action="data/save/document_version" name="document_version">'
            box = box + '<input name="rev_id" type=hidden value=' + str(version.id) + '>\n'
            box = box + '<input name="doc_id" type=hidden value=' + str(version.doc_id) + '>\n'
            box = box + '<tr>\n'
            box = box + '<td><input type=text name=version value="' + version.version + '"></td>\n'
            box = box + '<td><input type=text name=pub_date value="' + version.pub_date + '"></td>\n'
            box = box + '<td><input type=text name=initials size=3 maxlength=3 value="' + version.initials + '"></td>\n'
            box = box + '<td style="width:100%"><textarea name="notes" wrap=soft style="width:100%; height:100%">' + version.notes + '</textarea></td>\n'
            box = box + '<td><input type=checkbox name="delete">Del</td>\n'
            box = box + '<td><input type=submit name="action" value="|strsave|"></td>\n'
            box = box + '</tr>\n'
            box = box + '</form>\n'
        box = box + '<form method=GET action="data/save/newdocument_version" name="document_version">'
        box = box + '<input name="doc_id" type=hidden value=' + str(doc.id) + '>\n'
        box = box + '''
        <tr>
        <td><input type="text" name="version"></td>
        <td><input type="text" name="pub_date"></td>
        <td><input type="text" name="initials" size="3" maxlength="3"></td>
        <td style="width:100%"><textarea name="notes" wrap="soft" style="width:100%; height:100%"></textarea></td>
        <td></td><td><input type="submit" name="action" value="|stradd|"></td>
        </tr>
        </form>
        </table>
        '''
        return box
        

    def docfiles(self, uri, user):
        if not user:
            return '|blknopermission|'
        elif user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating docfiles table')
        doc = lampadas.docs[uri.id]
        box = '''
        <table class="box" width="100%">
        <tr><th colspan="5">|strdocfiles|</th></tr>
        <tr>
        <th class="collabel">|strfilename|</th>
        <th class="collabel">|strprimary|</th>
        <th class="collabel">|strformat|</th>
        <th class="collabel" colspan="2">|straction|</th>
        </tr>
        '''
        doc = lampadas.docs[uri.id]
        keys = doc.files.sort_by('filename')
        for key in keys:
            file = doc.files[key]
            box = box + '<form method=GET action="data/save/document_file" name="document_file">'
            box = box + '<input name="doc_id" type=hidden value=' + str(doc.id) + '>\n'
            box = box + '<input type=hidden name="filename" size=30 style="width:100%" value="' + file.filename + '">\n'
            box = box + '<tr>\n'
            if file.errors.count() > 0:
                box = box + '<td class="error">' + file.filename + '</td>\n'
            else:
                box = box + '<td>' + file.filename + '</td>\n'
            box = box + '<td>'  + combo_factory.tf('top', file.top, uri.lang) + '</td>\n'
            box = box + '<td>'  + combo_factory.format(file.format_code, uri.lang) + '</td>\n'
            box = box + '''
            <td><input type="checkbox" name="delete">|strdelete|</td>
            <td><input type="submit" name="action" value="|strsave|">
            </td>
            </tr>
            </form>
            '''
        box = box + '<form method=GET action="data/save/newdocument_file" name="document_file">'
        box = box + '<input name="doc_id" type="hidden" value="' + str(doc.id) + '">\n'
        box = box + '<tr>\n'
        box = box + '<td><input type="text" name="filename" size="30" style="width:100%"></td>\n'
        box = box + '<td>'  + combo_factory.tf('top', 0, uri.lang) + '</td>\n'
        box = box + '<td>'  + combo_factory.format('', uri.lang) + '</td>\n'
        box = box + '''
        <td></td>
        <td><input type="submit" name="action" value="|stradd|"></td>
        </tr>
        </form>
        </table>
        '''
        return box
        

    def docusers(self, uri, user):
        if not user:
            return '|blknopermission|'
        elif user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating docusers table')
        doc = lampadas.docs[uri.id]
        box = '''
        <table class="box" width="100%">
        <tr><th colspan="6">|strdocusers|</th></tr>
        <tr>
        <th class="collabel">|strusername|</th>
        <th class="collabel">|stractive|</th>
        <th class="collabel">|strrole|</th>
        <th class="collabel">|stremail|</th>
        <th class="collabel" colspan="2">|straction|</th>
        </tr>
        '''
        doc = lampadas.docs[uri.id]
        keys = doc.users.sort_by('username')
        for key in keys:
            docuser = doc.users[key]
            box = box + '<form method=GET action="data/save/document_user" name="document_user">'
            box = box + '<input type=hidden name="doc_id" value=' + str(doc.id) + '>\n'
            box = box + '<input type=hidden name="username" value=' + docuser.username + '>\n'
            box = box + '<tr>\n'
            box = box + '<td>' + docuser.username + '</td>\n'
            box = box + '<td>' + combo_factory.tf('active', docuser.active, uri.lang) + '</td>\n'
            box = box + '<td>' + combo_factory.role(docuser.role_code, uri.lang) + '</td>\n'
            box = box + '<td><input type=text name=email size=15 value="' +docuser.email + '"></td>\n'
            box = box + '<td><input type=checkbox name="delete">Del</td>\n'
            box = box + '<td><input type=submit name="action" value="|strsave|"></td>\n'
            box = box + '</tr>\n'
            box = box + '</form>\n'
        box = box + '<form method=GET action="data/save/newdocument_user" name="document_user">'
        box = box + '<input name="doc_id" type=hidden value=' + str(doc.id) + '>\n'
        box = box + '<tr>\n'
        box = box + '<td>' + '<input type=text name="username"></td>\n'
        box = box + '<td>' + combo_factory.tf('active', 1, uri.lang) + '</td>\n'
        box = box + '<td>' + combo_factory.role('', uri.lang) + '</td>\n'
        box = box + '<td><input type=text name=email size=15></td>\n'
        box = box + '<td></td><td><input type=submit name="action" value="|stradd|"></td>'
        box = box + '</tr>\n'
        box = box + '</form>\n'
        box = box + '</table>\n'
        return box
        

    def doctopics(self, uri, user):
        if not user:
            return '|blknopermission|'
        elif user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating doctopics table')
        doc = lampadas.docs[uri.id]
        box = ''
        box = box + '<table class="box" width="100%">'
        box = box + '<tr><th colspan="2">|strdoctopics|</th></tr>\n'
        box = box + '<tr>\n'
        box = box + '<th class="collabel">|strtopic|</th>\n'
        box = box + '<th class="collabel">|straction|</th>\n'
        box = box + '</tr>\n'
        doc = lampadas.docs[uri.id]
        topic_codes = lampadas.topics.sort_by('num')
        subtopic_codes = lampadas.subtopics.sort_by('num')
        for topic_code in topic_codes:
            for subtopic_code in subtopic_codes:
                if lampadas.subtopics[subtopic_code].topic_code==topic_code:
                    doctopic = doc.topics[subtopic_code]
                    if doctopic:
                        box = box + '<form method=GET action="data/save/deldocument_topic" name="document_topic">'
                        box = box + '<input type=hidden name="doc_id" value=' + str(doc.id) + '>\n'
                        box = box + '<input type=hidden name="subtopic_code" value=' + str(doctopic.subtopic_code) + '>\n'
                        box = box + '<tr>\n'
                        box = box + '<td>' + lampadas.topics[topic_code].name[uri.lang] + ': ' + lampadas.subtopics[doctopic.subtopic_code].name[uri.lang] + '</td>\n'
                        box = box + '<td><input type=submit name="action" value="|strdelete|"></td>\n'
                        box = box + '</tr>\n'
                        box = box + '</form>\n'
        box = box + '<form method=GET action="data/save/newdocument_topic" name="document_topic">'
        box = box + '<input name="doc_id" type=hidden value=' + str(doc.id) + '>\n'
        box = box + '<tr>\n'
        box = box + '<td>' + combo_factory.subtopic('', uri.lang) + '</td>\n'
        box = box + '<td><input type=submit name="action" value="|stradd|"></td>'
        box = box + '</tr>\n'
        box = box + '</form>\n'
        box = box + '</table>\n'
        return box


    def docnotes(self, uri, user):
        if not user:
            return '|blknopermission|'
        elif user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating docnotes table')
        doc = lampadas.docs[uri.id]
        box = ''
        box = box + '<table class="box" width="100%">'
        box = box + '<tr><th colspan="4">|strdocnotes|</th></tr>\n'
        box = box + '<tr>\n'
        box = box + '<th class="collabel">|strdate_time|</th>\n'
        box = box + '<th class="collabel">|strusername|</th>\n'
        box = box + '<th class="collabel">|strcomments|</th>\n'
        box = box + '</tr>\n'
        doc = lampadas.docs[uri.id]
        note_ids = doc.notes.sort_by('date_entered')
        for note_id in note_ids:
            note = doc.notes[note_id]
            box = box + '<tr>\n'
            box = box + '<td>' + note.date_entered + '</td>\n'
            box = box + '<td>' + note.creator + '</td>\n'
            box = box + '<td>' + note.notes + '</td>\n'
            box = box + '</tr>\n'
        box = box + '<form method=GET action="data/save/newdocument_note" name="document_note">'
        box = box + '<input name="doc_id" type=hidden value=' + str(doc.id) + '>\n'
        box = box + '<input name="creator" type=hidden value=' + user.username + '>\n'
        box = box + '<tr><td></td><td></td>\n'
        box = box + '<td><textarea name="notes" rows=5 cols=40></textarea></td>\n'
        box = box + '<td><input type=submit name="action" value="|stradd|"></td>'
        box = box + '</tr>\n'
        box = box + '</form>\n'
        box = box + '</table>\n'
        return box


    def errors(self, uri, user):
        """
        Builds a complete list of all errors reported by Lintadas.
        It uses docerrors() and docfileerrors(), and just concatenates
        all of their contents.
        """

        if not user:
            return '|blknopermission|'

        log(3, 'Creating errors table')
        doc_ids = lampadas.docs.sort_by('title')
        box = ' '
        for doc_id in doc_ids:
            doc = lampadas.docs[doc_id]

            # Only display docs the user has rights to.
            if user.can_edit(doc_id=doc_id)==0:
                continue
            if doc.lang==uri.lang:
                show_doc = 0
                show_files = 0
                if doc.errors.count() > 0:
                    show_doc = 1
                else:
                    filenames = doc.files.keys()
                    for filename in filenames:
                        if doc.files[filename].errors.count() > 0:
                            show_files = 1
                            break
                if show_doc==1 or show_files==1:
                    box = box + '<h1>' + doc.title + '</h1>'
                    uri.id = doc_id
                if show_doc==1:
                    box = box + '<p>' + self.docerrors(uri, user)
                if show_files==1:
                    box = box + '<p>' + self.docfileerrors(uri, user)
        return box


    def docerrors(self, uri, user):
        if not user:
            return '|blknopermission|'
        elif user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating docerrors table')
        doc = lampadas.docs[uri.id]
        box = ''
        box = box + '<table class="box" width="100%">'
        box = box + '<tr><th colspan="2">|strdocerrs|</th></tr>\n'
        box = box + '<tr>\n'
        box = box + '<th class="collabel">|strid|</th>\n'
        box = box + '<th class="collabel">|strerror|</th>\n'
        box = box + '</tr>\n'
        err_ids = doc.errors.sort_by('date_entered')
        for err_id in err_ids:
            docerror = doc.errors[err_id]
            error = lampadas.errors[err_id]
            box = box + '<tr>\n'
            box = box + '<td>' + str(docerror.err_id) + '</td>\n'
            box = box + '<td>' + error.name[uri.lang] + '</td>\n'
            box = box + '</tr>\n'
        box = box + '</table>\n'
        return box


    def docfileerrors(self, uri, user):
        if not user:
            return '|blknopermission|'
        elif user.can_edit(doc_id=uri.id)==0:
            return '|blknopermission|'

        log(3, 'Creating docfileerrors table')
        doc = lampadas.docs[uri.id]
        box = ''
        box = box + '<table class="box" width="100%">'
        box = box + '<tr><th colspan="3">|strfileerrs|</th></tr>\n'
        box = box + '<tr>\n'
        box = box + '<th class="collabel">|strid|</th>\n'
        box = box + '<th class="collabel">|strfilename|</th>\n'
        box = box + '<th class="collabel">|strerror|</th>\n'
        box = box + '</tr>\n'
        filenames = doc.files.sort_by('filename')
        for filename in filenames:
            file = doc.files[filename]
            err_ids = file.errors.sort_by('date_entered')
            for err_id in err_ids:
                fileerror = file.errors[err_id]
                error = lampadas.errors[err_id]
                box = box + '<tr>\n'
                box = box + '<td>' + str(fileerror.err_id) + '</td>\n'
                box = box + '<td>' + error.name[uri.lang] + '</td>\n'
                box = box + '</tr>\n'
        box = box + '</table>\n'
        return box


    def cvslog(self, uri):
        doc = lampadas.docs[uri.id]
        box = '<table class="box" width="100%">\n'
        box = box + '<tr><th>|strcvslog|</th></tr>\n'
        box = box + '<tr><td>\n'
        cvsdir = config.cvs_root + str(doc.id)

        # FIXME: finish this.

        box = box + '</td></tr>\n'
        box = box + '</table>\n'
        return box

    def letters(self, uri):
        log(3, 'Creating letter table')
        box = '<table class="box"><tr>\n'
        for letter in string.uppercase:
            if letter==uri.letter:
                box = box + '<th>' + letter + '</th>\n'
            else:
                box = box + '<th><a href="' + uri.filename + '|uri.lang_ext|/' + letter + '">' + letter + '</a></th>\n'
        box = box + '</tr></table>\n'
        return box
        
    def users(self, uri, build_user):
        log(3, 'Creating users table')
        box = '<table class="box"><tr><th colspan=2>|strusers|</th></tr>\n'
        box = box + '<tr>\n'
        box = box + '<th class="collabel">|strusername|</th>\n'
        box = box + '<th class="collabel">|strname|</th>\n'
        box = box + '</tr>\n';
        if uri.letter > '':
            usernames = lampadas.users.letter_keys(uri.letter)
            for username in usernames:
                user = lampadas.users[username]
                box = box + '<tr>\n'
                box = box + '<td><a href="/user|uri.lang_ext|/' + username + '">' + username + '</a></td>\n'
                box = box + '<td>' + user.name + '</a></td>\n'
                box = box + '</tr>\n'
        box = box + '</table>\n'
        return box

    def user(self, uri, build_user):
        if not build_user:
            return '|blknopermission|'
        elif build_user.can_edit(username=uri.username)==0:
            return '|blknopermission|'

        if uri.username > '':
            user = lampadas.users[uri.username]
            if user==None:
                return '|blknotfound|'
            box = '<form method=GET action="data/save/user" name="user">\n'
        else:
            user = User()
            box = '<form method=GET action="data/save/newuser" name="user">\n'
        box = box + '<table class="box" width="100%">\n'
        box = box + '<tr><th colspan=2>|struserdetails|</th><th>|strcomments|</th></tr>\n'
        box = box + '<tr><th class="label">|strusername|</th>'
        if user.username=='':
            box = box + '<td><input type=text name="username"></td>\n'
        else:
            box = box + '<td><input name="username" type=hidden value=' + uri.username + '>' + uri.username + '</td>\n'
        box = box + '<td rowspan=10 style="width:100%"><textarea name="notes" wrap=soft style="width:100%; height:100%">' + user.notes + '</textarea></td></tr>\n'
        box = box + '<tr><th class="label">|strfirst_name|</th><td><input type=text name=first_name size="15" value="' + user.first_name + '"></td></tr>\n'
        box = box + '<tr><th class="label">|strmiddle_name|</th><td><input type=text name=middle_name size="15" value="' + user.middle_name + '"></td></tr>\n'
        box = box + '<tr><th class="label">|strsurname|</th><td><input type=text name=surname size="15" value="' + user.surname + '"></td></tr>\n'
        box = box + '<tr><th class="label">|stremail|</th><td><input type=text name=email size="15" value="' + user.email + '"></td></tr>\n'
        box = box + '<tr><th class="label">|strstylesheet|</th><td><input type=text name=stylesheet size="12" value="' + user.stylesheet + '"></td></tr>\n'
        box = box + '<tr><th class="label">'
        if user.username=='':
            box = box + '|strpassword|'
        else:
            box = box + '|strnewpassword|'
        box = box + '</th><td><input type=text name=password size="12"></td></tr>\n'
        if build_user and build_user.admin > 0 or build_user.sysadmin > 0:
            box = box + '<tr><th class="label">|stradmin|</th><td>' + combo_factory.tf('admin', user.admin, uri.lang) + '</td></tr>\n'
            box = box + '<tr><th class="label">|strsysadmin|</th><td>' + combo_factory.tf('sysadmin', user.sysadmin, uri.lang) + '</td></tr>\n'
        else:
            box = box + '<input name="admin" type="hidden" value="' + str(user.admin) + '">\n'
            box = box + '<input name="sysadmin" type="hidden" value="' + str(user.sysadmin) + '">\n'
            box = box + '<tr><th class="label">|stradmin|</th><td>' + bool2yesno(user.admin) + '</td></tr>\n'
            box = box + '<tr><th class="label">|strsysadmin|</th><td>' + bool2yesno(user.sysadmin) + '</td></tr>\n'
        box = box + '<tr><td></td><td><input type=submit name=save value=|strsave|></td></tr>\n'
        box = box + '</table>\n'
        box = box + '</form>\n'
        return box
        
    def doctable(self, uri, user, type_code=None, subtopic_code=None, username=None, maintained=None, maintainer_wanted=None, pub_status_code=None):
        log(3, "Creating doctable")
        box = '<table class="box" width="100%"><tr><th colspan="2">|strtitle|</th></tr>'
        keys = lampadas.docs.sort_by("title")
        for key in keys:
            doc = lampadas.docs[key]
            ok = 1

            # If a usename is passed in, do not filter by language.
            # We're building the user's personal doctable, so language
            # doesn't matter in that table.
            if username:
                if doc.users[username]==None:
                    ok = 0
            else:
                if doc.lang <> uri.lang:
                    ok = 0

            # If any other parameters were specified, limit the documents
            # to those which match the requirements.
            if type_code and doc.type_code <> type_code:
                ok = 0
            if subtopic_code:
                subtopic = lampadas.subtopics[subtopic_code]
                if subtopic.docs[doc.id]==None:
                    ok = 0
            if not maintained==None:
                if doc.maintained <> maintained:
                    ok = 0
            if not maintainer_wanted==None:
                if doc.maintainer_wanted <> maintainer_wanted:
                    ok = 0
            if not pub_status_code==None:
                if doc.pub_status_code <> pub_status_code:
                    ok = 0

            # Build the table for any documents that passed the filters
            if ok > 0:
                box = box + '<tr><td>'
                if user and user.can_edit(doc_id=doc.id):
                    box = box + '<a href="editdoc|uri.lang_ext|/' + str(doc.id) + '">' + EDIT_ICON + '</a>'
                box = box + '</td>\n'
                box = box + '<td style="width:100%"><a href="doc/' + str(doc.id) + '/">' + doc.title + '</a></td>'
                box = box + '</tr>\n'
        box = box + '</table>'
        return box

    def user_docs(self, uri, user):
        if user:
            box = self.doctable(uri, user, username=user.username)
        else:
            box = '|nopermission|'
        return box

    def section_menu(self, uri, user, section_code):
        log(3, "Creating section menu: " + section_code)
        section = lampadasweb.sections[section_code]
        box = '<table class="navbox"><tr><th>' + section.name[uri.lang] + '</th></tr>\n'
        box = box + '<tr><td>'
        keys = lampadasweb.pages.sort_by('sort_order')
        for key in keys:
            page = lampadasweb.pages[key]
            if page.section_code==section.code:
                if page.only_registered or page.only_admin or page.only_sysadmin > 0:
                    if user==None:
                        continue
                if page.only_admin > 0:
                    if user.admin==0 and user.sysadmin==0:
                        continue
                if page.only_sysadmin > 0:
                    if user.sysadmin==0:
                        continue
                box = box + '<a href="' + page.code + '|uri.lang_ext|">' + page.menu_name[uri.lang] + '</a><br>\n'
        box = box + '</td></tr></table>\n'
        return box

    def section_menus(self, uri, user):
        log(3, "Creating all section menus")
        box = ''
        keys = lampadasweb.sections.sort_by('sort_order')
        first_menu = 1
        for key in keys:
            section = lampadasweb.sections[key]
            if section.only_registered or section.only_admin or section.only_sysadmin > 0:
                if user==None or section.registered_count==0:
                    continue
            if section.only_admin > 0:
                if (user.admin==0 and user.sysadmin==0) or (section.admin_count==0):
                    continue
            if section.only_sysadmin > 0:
                if user.sysadmin==0 or section.sysadmin_count==0:
                    continue
            if first_menu==1:
                first_menu = 0
            else:
                box = box + '<p>'
            box = box + self.section_menu(uri, user, section.code)
        return box

    def sitemap(self, uri, user):
        log(3, 'Creating sitemap')
        box = ''
        box = '<table class="box" width="100%"><tr><th colspan="2">|strsitemap|</th></tr>\n'
        section_codes = lampadasweb.sections.sort_by('sort_order')
        page_codes = lampadasweb.pages.sort_by('sort_order')
        for section_code in section_codes:
            section = lampadasweb.sections[section_code]
            if section.only_registered or section.only_admin or section.only_sysadmin > 0:
                if user==None or section.registered_count==0:
                    continue
            if section.only_admin > 0:
                if (user.admin==0 and user.sysadmin==0) or (section.admin_count==0):
                    continue
            if section.only_sysadmin > 0:
                if user.sysadmin==0 or section.sysadmin_count==0:
                    continue

            box = box + '<tr><td class="label">' +  section.name[uri.lang] + '</td><td>\n'
            for page_code in page_codes:
                page = lampadasweb.pages[page_code]
                if page.section_code==section_code:
                    if page.only_registered or page.only_admin or page.only_sysadmin > 0:
                        if user==None:
                            continue
                    if page.only_admin > 0:
                        if user.admin==0 and user.sysadmin==0:
                            continue
                    if page.only_sysadmin > 0:
                        if user.sysadmin==0:
                            continue
                    box = box + '<a href="/' + page.code + '|uri.lang_ext|">' + page.menu_name[uri.lang] + '</a><br>\n'
            box = box + '</td></tr>\n'
        box = box + '</table>\n'
        return box

# FIXME WOStringIO implemented below --nico

    def recent_news(self, uri):
        log(3, 'Creating recent news')
        box = WOStringIO('''<table class="box" width="100%">
        <tr><th>|strdate|</th><th>|strnews|</th></tr>\n''')
        keys = lampadasweb.news.sort_by_desc('pub_date')
        for key in keys:
            news = lampadasweb.news[key]
            if not news.news[uri.lang]==None:
                box.write('''<tr><td>%s</td><td>%s</td></tr>\n'''
                          % (news.pub_date, news.news[uri.lang]))
        box.write('</table>\n')
        return box.get_value()

    def topics(self, uri):
        log(3, 'Creating topics menu')
        box = WOStringIO('''<table class="navbox">
        <tr><th>|strtopics|</th></tr>
        <tr><td><ol>''')
        keys = lampadas.topics.sort_by('num')
        for key in keys:
            topic = lampadas.topics[key]
            box.write('<li><a href="topic|uri.lang_ext|/%s">%s</a></li>\n'
                      % (topic.code, topic.name[uri.lang]))
        box.write('</ol></td></tr></table>\n')
        return box.get_value()

    def subtopics(self, uri):
        log(3, 'Creating subtopics menu')
        topic = lampadas.topics[uri.code]
        box = WOStringIO('''<table class="box" width="100%%">
        <tr><th>%s</th></tr>
        <tr><td>|topic.description|</td></tr>
        <tr><td><ol>
        ''' % topic.name[uri.lang] )
        keys = lampadas.subtopics.sort_by('num') 
        for key in keys:
            subtopic = lampadas.subtopics[key]
            if subtopic.topic_code==uri.code:
                box.write('<li><a href="subtopic|uri.lang_ext|/%s">%s</a>\n'
                          % (subtopic.code, subtopic.name[uri.lang]))
        box.write('</ol></td></tr>\n</table>\n')
        return box.get_value()

    def subtopic(self, uri):
        log(3, 'Creating subtopic table')
        subtopic = lampadas.subtopics[uri.code]
        box = '''<table class="box" width="100%%">
        <tr><th>%s</th></tr>
        <tr><td>%s</td><tr>
        </table>
        ''' % (subtopic.name[uri.lang], subtopic.description[uri.lang])
        return box

    def types(self, uri):
        log(3, 'Creating types menu')
        box = WOStringIO('''<table class="navbox">
        <tr><th>|strtypes|</th></tr>
        <tr><td>''')
        keys = lampadas.types.sort_by('sort_order')
        for key in keys:
            type = lampadas.types[key]
            box.write('<a href="type|uri.lang_ext|/%s">%s</a><br>\n'
                      % (type.code, type.name[uri.lang]))
        box.write('</td></tr>\n</table>\n')
        return box.get_value()

    def login(self, uri, user):
        if user:
            log(3, 'Creating active user box')
            box = '''<table class="navbox">
            <tr><th>|stractive_user|</th></tr>
            <form name="logout" action="data/session/logout">
            <input name="username" type="hidden" value="%s">
            <tr><td align="center">
            <a href="/user|uri.lang_ext|/|session_username|">|session_name|</a>
            </td></tr>
            <tr><td align="center"><input type="submit" name="logout"
            value="|strlog_out|"></td></tr>
            </form>
            </table>
            ''' % user.username
        else:
            log(3, 'Creating login box')
            box = '''<table class="navbox">
            <tr><th colspan="2">|strlogin|</th></tr>
            <form name="login" action="data/session/login" method="GET">
            <tr>
              <td class="label">|strusername|</td>
              <td><input type="text" name="username" size="12"></td>
            </tr>
            <tr>
              <td class="label">|strpassword|</td>
              <td><input type="password" name="password" size="12"></td>
            </tr>
            <tr>
              <td align="center" colspan="2">
              <input type=submit name="login" value="login"><br>
              <a href="mailpass|uri.lang_ext|">|strmail_passwd|</a><br>
              <a href="newuser|uri.lang_ext|">|strcreate_acct|</a></td>
            </tr>
            </form> 
            </table>
            '''
        return box

    def navsessions(self, uri, user):
        if user and user.admin > 0:
            log(3, 'Creating navsessions table')
            box = WOStringIO('''<table class="navbox">
            <tr><th>|strsessions|</th></tr>
            <tr><td>
            ''')
            keys = sessions.sort_by('username')
            for key in keys:
                session = sessions[key]
                box.write('<a href="user|uri.lang_ext|/%s">%s</a><br>\n'
                          % (session.username, session.username))
            box.write('</td></tr>\n</table>\n')
            return box.get_value()
        return ' '

    def tabsessions(self, uri, user):
        if user and user.admin > 0:
            log(3, 'Creating sessions table')
            box = WOStringIO('''<table class="box">
            <tr><th colspan="4">|strsessions|</th></tr>
            <tr>
            <th class="collabel">|strusername|</th>
            <th class="collabel">|strip_address|</th>
            <th class="collabel">|strurl|</th>
            <th class="collabel">|strtimestamp|</th>
            </tr>
            ''')
            keys = sessions.sort_by_desc('timestamp')
            for key in keys:
                session = sessions[key]
                box.write('''<tr>
                <td><a href="user|uri.lang_ext|/%s">%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                </tr>
                ''' % (session.username, session.username,
                       session.ip_address,
                       session.uri,
                       session.timestamp))
            box.write('</table>\n')
            return box.get_value()
        return '|nopermission|'

    def languages(self, uri):
        log(3, 'Creating languages table')
        box = WOStringIO('''<table class="navbox">
        <tr><th>|strlanguages|</th></tr>
        <tr><td>
        ''')
        keys = lampadas.languages.sort_by_lang('name', uri.lang)
        for key in keys:
            language = lampadas.languages[key]
            if language.supported > 0:
                if uri.data > '':
                    add_data = '/' + uri.data
                else:
                    add_data = ''
                box.write('<a href="/%s.%s%s">%s</a><br>\n'
                          % (uri.filename, language.code.lower(),
                             add_data, language.name[uri.lang]))
        box.write('</td></tr>\n</table>\n')
        return box.get_value()

    def tabmailpass(self, uri):
        log(3, 'Creating mailpass table')
        box = '''<form name="mailpass" action="data/save/mailpass">
        <table class="box">
        <tr><th colspan="2">|strmail_passwd|</th></tr>
        <tr>
        <td><input type="text" name="email"></td>
        <td align="center"><input type="submit" name="mailpass" value="|strmail_passwd|"></td></tr>
        </table>
        </form>
        '''
        return box

# PageFactory

class PageFactory:

    tablef  = TableFactory()

    def page_exists(self, key):
        uri = URI(key)
        if uri.path=='' and lampadasweb.pages[uri.filename]:
            return 1
        return

    def page(self, uri, session=None):
        build_user = None
        if session:
            build_user = lampadas.users[session.username]
            log(3, 'build_user: ' + build_user.username)

        page = lampadasweb.pages[uri.filename]
        if page==None:
            page = lampadasweb.pages['404']
        assert not page==None
        html = self.build_page(page, uri, build_user)

        return html
    

    def build_page(self, page, uri, build_user):
        template = lampadasweb.templates[page.template_code]
        assert not template==None
        html = template.template

        html = html.replace('\|', 'DCM_PIPE')
    
        pos = html.find('|')
        while pos <> -1 :
            pos2 = html.find('|', pos+1)
            if pos2==-1:
                pos = -1
            else:
                oldstring = html[pos:pos2+1]
                token = html[pos+1:pos2]

                newstring = None
            
                # Tokens based on a logged-in user
                # 
                if token=='session_id':
                    if build_user==None:
                        newstring = ''
                    else:
                        newstring = build_user.session_id
                if token=='session_username':
                    if build_user==None:
                        newstring = ''
                    else:
                        newstring = build_user.username
                if token=='session_name':
                    if build_user==None:
                        newstring = ''
                    else:
                        newstring = build_user.name
                if token=='session_user_docs':
                    newstring = self.tablef.user_docs(uri, build_user)

                # Meta-data about the page being served
                # 
                if token=='title':
                    newstring = page.title[uri.lang]
                if token=='body':
                    newstring = page.page[uri.lang]
                if token=='base':
                    newstring = 'http://' + config.hostname
                    if config.port > '':
                        newstring = newstring + ':' + config.port
                    newstring = newstring + config.root_dir
                    if uri.force_lang:
                        newstring = newstring + uri.lang + '/'

                # Meta-data from the page's URL
                if token=='uri.lang_ext':
                    newstring = uri.lang_ext
                if token=='uri.code':
                    newstring = uri.code
                if token=='uri.base':
                    newstring = uri.base


                # Configuration information
                # 
                if token=='hostname':
                    newstring = config.hostname
                if token=='rootdir':
                    newstring = config.root_dir
                if token=='port':
                    newstring = str(config.port)
                if token=='stylesheet':
                    if build_user:
                        newstring = build_user.stylesheet
                    else:
                        newstring='default'
                if token=='version':
                    newstring = VERSION

                # Tokens for when a page embeds an object
                # 
                if token=='user.username':
                    user = lampadas.users[uri.username]
                    if not user:
                        newstring = '|blknotfound|'
                    else:
                        newstring = user.username
                if token=='user.name':
                    user = lampadas.users[uri.username]
                    if not user:
                        newstring = '|blknotfound|'
                    else:
                        newstring = user.name
                if token=='type.name':
                    type = lampadas.types[uri.code]
                    if not type:
                        newstring = '|blknotfound|'
                    else:
                        newstring = type.name[uri.lang]
                if token=='topic.name':
                    topic = lampadas.topics[uri.code]
                    if not topic:
                        newstring = '|blknotfound|'
                    else:
                        newstring = topic.name[uri.lang]
                if token=='topic.description':
                    topic = lampadas.topics[uri.code]
                    if not topic:
                        newstring = '|blknotfound|'
                    else:
                        newstring = topic.description[uri.lang]

                # Navigation Boxes
                # 
                if token=='navlogin':
                    newstring = self.tablef.login(uri, build_user)
                if token=='navmenus':
                    newstring = self.tablef.section_menus(uri, build_user)
                if token=='navtopics':
                    newstring = self.tablef.topics(uri)
                if token=='navtypes':
                    newstring = self.tablef.types(uri)
                if token=='navsessions':
                    newstring = self.tablef.navsessions(uri, build_user)
                if token=='navlanguages':
                    newstring = self.tablef.languages(uri)

                # Tables
                # 
                if token=='tabsubtopics':
                    newstring = self.tablef.subtopics(uri)
                if token=='tabdocs':
                    newstring = self.tablef.doctable(uri, build_user)
                if token=='tabmaint_wanted':
                    newstring = self.tablef.doctable(uri, build_user, maintainer_wanted=1)
                if token=='tabunmaintained':
                    newstring = self.tablef.doctable(uri, build_user, maintained=0)
                if token=='tabpending':
                    newstring = self.tablef.doctable(uri, build_user, pub_status_code='P')
                if token=='tabwishlist':
                    newstring = self.tablef.doctable(uri, build_user, pub_status_code='W')
                if token=='tabeditdoc':
                    newstring = self.tablef.doc(uri, build_user)
                if token=='tabdocfiles':
                    newstring = self.tablef.docfiles(uri, build_user)
                if token=='tabdocusers':
                    newstring = self.tablef.docusers(uri, build_user)
                if token=='tabdocversions':
                    newstring = self.tablef.docversions(uri, build_user)
                if token=='tabdoctopics':
                    newstring = self.tablef.doctopics(uri, build_user)
                if token=='tabdocerrors':
                    newstring = self.tablef.docerrors(uri, build_user)
                if token=='tabdocfileerrors':
                    newstring = self.tablef.docfileerrors(uri, build_user)
                if token=='tabdocnotes':
                    newstring = self.tablef.docnotes(uri, build_user)
                if token=='tabcvslog':
                    newstring = self.tablef.cvslog(uri)
                if token=='tabletters':
                    newstring = self.tablef.letters(uri)
                if token=='tabusers':
                    newstring = self.tablef.users(uri, build_user)
                if token=='tabuser':
                    newstring = self.tablef.user(uri, build_user)
                if token=='tabrecentnews':
                    newstring = self.tablef.recent_news(uri)
                if token=='tabsubtopic':
                    newstring = self.tablef.subtopic(uri)
                if token=='tabtypedocs':
                    newstring = self.tablef.doctable(uri, build_user, type_code=uri.code)
                if token=='tabsubtopicdocs':
                    newstring = self.tablef.doctable(uri, build_user, subtopic_code=uri.code)
                if token=='tabsitemap':
                    newstring = self.tablef.sitemap(uri, build_user)
                if token=='tabsessions':
                    newstring = self.tablef.tabsessions(uri, build_user)
                if token=='tabmailpass':
                    newstring = self.tablef.tabmailpass(uri)
                if token=='taberrors':
                    newstring = self.tablef.errors(uri, build_user)
            
                # Blocks and Strings
                # 
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
                # 
                if newstring==None:
                    log(1, 'Could not replace token ' + token)
                    newstring = 'ERROR (' + token + ')'
                
                html = html.replace(html[pos:pos2+1], newstring)
                html = html.replace('\|', 'DCM_PIPE')
                
                pos = html.find('|')
        
        html = html.replace('DCM_PIPE', '|')
    
        return html


page_factory = PageFactory()
combo_factory = ComboFactory()

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

