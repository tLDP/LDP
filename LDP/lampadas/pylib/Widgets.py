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

This module generates HTML primitives.
"""

from Globals import *
from Log import log
from DataLayer import lampadas
from Languages import languages
import re
import string


class Widgets:
    """
    Generates low level widgets for use in constructing web pages. The use of
    the term "widget" is very loose since we also use this class to generate
    standard formats for some text items.
    """

    def title(self, value):
        return WOStringIO('<input type=text name="title" style="width:100%%" value="%s">' % value).get_value()

    def title_compressed(self, value):
        """
        Compress the title so it will display well in 80 characters.
        Just add spaces around all + signs, which lets the title wrap.
        """
        
        parts = value.split('+')
        text = string.join(parts, ' + ')
        return text
        
    def short_title(self, value):
        return WOStringIO('<input type=text name="short_title" style="width:100%%" value="%s">' % value).get_value()

    def abstract(self, value):
        return '<input type=text name="abstract" style="width:100%" value="' + value + '">'

    def short_desc(self, value):
        return '<input type=text name="short_desc" style="width:100%" value="' + value + '">'

    def pub_date(self, value):
        return '<input type=text name="pub_date" width="10" maxlength="10" value="' + value + '">'

    def last_update(self, value):
        return '<input type=text name="last_update" width="10"  maxlength="10" value="' + value + '">'

    def tickle_date(self, value):
        return '<input type=text name="tickle_date" width="10" maxlength="10" value="' + value + '">'

    def isbn(self, value):
        return '<input type=text name="isbn" width="13" maxlength="13" value="' + value + '">'

    def rating(self, value):
        return '<input type=text name="rating" width="2" maxlength="2" value="' + value + '">'

    def copyright_holder(self, value):
        return '<input type=text name="copyright_holder" width="20" value="' + value + '">'

    def tf(self, name, value, lang):
        if value==1:
            v1, v2 = ' selected', ''
        elif value==0:
            v1, v2 = '', ' selected'
        else:
            v1, v2 = '', ''
        return WOStringIO('<select name="%s">\n' \
                          '<option></option>\n' \
                          '<option value="1"%s>|stryes|</option>\n' \
                          '<option value="0"%s>|strno|</option>\n' \
                          '</select>\n'
                          % (name, v1, v2)).get_value()

    def doctable_layout(self, value='compact'):
        if value=='compact':
            compact, expanded = ' selected', ''
        elif value=='expanded':
            compact, expanded = '', ' selected'
        else:
            compact, expanded = 'compact', ''
        return WOStringIO('<select name="%s">\n' \
                          '<option value="compact"%s>|strcompact_layout|</option>\n' \
                          '<option value="expanded"%s>|strexpanded_layout|</option>\n' \
                          '</select>\n'
                          % ('layout', compact, expanded)).get_value()


    def username(self, value):
        return '<input type=text name="username" width="15" maxlength="40" value="' + value + '">'

    def stylesheet(self, value):
        return '<select name="stylesheet">\n</select>\n'
    
    def role_code(self, value, lang):
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

    def collection_code(self, value, lang):
        combo = WOStringIO("<select name='collection_code'>\n" \
                           "<option></option>\n")
        keys = lampadas.collections.sort_by('sort_order')
        for key in keys:
            collection = lampadas.collections[key]
            assert not collection==None
            combo.write("<option ")
            if collection.code==value:
                combo.write("selected ")
            combo.write("value='%s'>%s</option>\n"
                        % (collection.code, collection.name[lang]))
        combo.write("</select>")
        return combo.get_value()

    def type_code(self, value, lang):
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

    def doc_id(self, value, lang):
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

    def sk_seriesid(self, value):
        combo = WOStringIO('<select name="sk_seriesid">\n')
        combo.write('<option></option>\n')
        keys = lampadas.docs.sort_by('title')
        for key in keys:
            doc = lampadas.docs[key]
            if doc.sk_seriesid > '':
                combo.write("<option ")
                if doc.sk_seriesid==value:
                    combo.write("selected ")
                if doc.short_title > '':
                    combo.write("value='%s'>%s</option>\n"
                                % (str(doc.sk_seriesid), doc.short_title + ' (' + doc.lang + ')'))
                else:
                    combo.write("value='%s'>%s</option>\n"
                                % (str(doc.sk_seriesid), doc.title[:40] + ' (' + doc.lang + ')'))
        combo.write("</select>\n")
        return combo.get_value()

    def replaced_by_id(self, value):
        combo = WOStringIO('<select name="replaced_by_id">\n')
        combo.write('<option></option>\n')
        keys = lampadas.docs.sort_by('title')
        for key in keys:
            doc = lampadas.docs[key]
            combo.write("<option ")
            if doc.id==value:
                combo.write("selected ")
            if doc.short_title > '':
                combo.write("value='%s'>%s</option>\n"
                            % (str(doc.id),doc.short_title))
            else:
                combo.write("value='%s'>%s</option>\n"
                            % (str(doc.id),doc.title[:40]))
        combo.write("</select>\n")
        return combo.get_value()

    def doc_lang(self, value, lang):
        combo = WOStringIO("<select name='lang'>\n")
        if value=='':
            combo.write('<option selected></option>')
        else:
            combo.write('<option></option>')
        keys = languages.sort_by_lang('name', lang)
        for key in keys:
            if lampadas.docs.languages[key] > 0:
                language = languages[key]
                assert not language==None
                combo.write("<option ")
                if language.code==value:
                    combo.write("selected ")
                combo.write("value='" + language.code + "'>")
                combo.write(language.name[lang])
                combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def lang(self, value, lang):
        combo = WOStringIO("<select name='lang'>\n")
        if value=='':
            combo.write('<option selected></option>')
        else:
            combo.write('<option></option>')
        keys = languages.sort_by_lang('name', lang)
        for key in keys:
            language = languages[key]
            assert not language==None
            combo.write("<option ")
            if language.code==value:
                combo.write("selected ")
            combo.write("value='" + language.code + "'>")
            combo.write(language.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def license_code(self, value, lang):
        combo = WOStringIO("<select name='license_code'>\n")
        combo.write('<option></option>')
        keys = lampadas.licenses.sort_by('sort_order')
        for key in keys:
            license = lampadas.licenses[key]
            assert not license==None
            combo.write("<option ")
            if license.code==value:
                combo.write("selected ")
            combo.write("value='" + license.code + "'>")
            combo.write(license.short_name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def page_code(self, value, lang):
        combo = WOStringIO("<select name='page_code'>\n")
        keys = lampadasweb.pages.sort_by('page_code')
        for key in keys:
            page = lampadasweb.pages[key]
            assert not page==None
            combo.write("<option ")
            if page.code==value:
                combo.write("selected ")
            combo.write("value='" + str(page.code) + "'>")
            combo.write(page.title[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def pub_status_code(self, value, lang):
        combo = WOStringIO("<select name='pub_status_code'>\n")
        combo.write('<option></option>')
        keys = lampadas.pub_statuses.sort_by('sort_order')
        for key in keys:
            pubstatus = lampadas.pub_statuses[key]
            assert not pubstatus==None
            combo.write("<option ")
            if pubstatus.code==value:
                combo.write("selected ")
            combo.write("value='" + pubstatus.code + "'>")
            combo.write(pubstatus.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()
        
    def format_code(self, value, lang):
        combo = WOStringIO("<select name='format_code'>\n")
        combo.write('<option></option>')
        keys = lampadas.formats.sort_by_lang('name', lang)
        for key in keys:
            format = lampadas.formats[key]
            assert not format==None
            combo.write("<option ")
            if format.code==value:
                combo.write("selected ")
            combo.write("value='" + format.code + "'>")
            combo.write(format.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()
        
    def dtd_code(self, value):
        combo = WOStringIO("<select name='dtd_code'>\n")
        if value=='':
            combo.write('<option selected></option>')
        else:
            combo.write('<option></option>')
        keys = lampadas.dtds.sort_by('code')
        for key in keys:
            dtd = lampadas.dtds[key]
            assert not dtd==None
            combo.write("<option ")
            if dtd.code==value:
                combo.write("selected ")
            combo.write("value='" + dtd.code + "'>")
            combo.write(dtd.code)
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()
        
    def review_status_code(self, value, lang):
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

    def tech_review_status_code(self, value, lang):
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

    def topic_code(self, value, lang):
        combo = WOStringIO('<select name="topic_code">\n')
        combo.write('<option></option>')
        topic_codes = lampadas.topics.sort_by('sort_order')
        for topic_code in topic_codes:
            topic = lampadas.topics[topic_code]
            combo.write("<option ")
            if topic.code==value:
                combo.write("selected ")
            combo.write("value='" + topic.code + "'>")
            combo.write(topic.title[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def filemode(self, value):
        if value > 0:
            return WOStringIO(octal2permission(value)).get_value()
        else:
            return '|strunknown|'

widgets = Widgets()
