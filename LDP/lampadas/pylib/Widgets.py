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
import re
import string

from CoreDM import dms

class Widgets:
    """
    Generates low level widgets for use in constructing web pages. The use of
    the term "widget" is very loose since we also use this class to generate
    standard formats for some text items.
    """

    def bar_graph(self, value, max, lang):
        return str(value) + '/' + str(max)

    def format_code(self, value, lang, view=0):
        if view==1:
            format = dms.format.get_by_id(value)
            if format:
                return format.name[lang]
            return ''

        combo = WOStringIO('<select name="format_code">\n')
        combo.write('<option></option>')
        formats = dms.format.get_all()
        for key in formats.sort_by_lang('name', lang):
            format = formats[key]
            combo.write("<option ")
            if format.code==value:
                combo.write("selected ")
            combo.write("value='" + format.code + "'>")
            combo.write(format.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()
        
    def dtd_code(self, value, lang, view=0):
        if view==1:
            dtd = dms.dtd.get_by_id(value)
            if dtd:
                return dtd.name[lang]
            return ''

        combo = WOStringIO('<select name="dtd_code">\n')
        if value=='':
            combo.write('<option selected></option>')
        else:
            combo.write('<option></option>')
        dtds = dms.dtd.get_all()
        for key in dtds.sort_by_lang('name', lang):
            dtd = dtds[key]
            combo.write("<option ")
            if dtd.code==value:
                combo.write("selected ")
            combo.write("value='" + dtd.code + "'>")
            combo.write(dtd.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()
        
    def dtd_version(self, value, view=0):
        input = WOStringIO('<input type="text" name="dtd_version" size="8" maxlenth="20" value="%s">' % (value))
        return input.get_value()

    def title(self, value, view=0):
        return '<input type=text name="title" style="width:100%%" value="%s">' % (escape_tokens(value))

    def abstract(self, value, view=0):
        return '<textarea name="abstract" rows="6" cols="20" style="width:100%%">%s</textarea>' % (html_encode(value))

    def news(self, value, view=0):
        return '<textarea name="news" rows="6" cols="20" style="width:100%%">%s</textarea>' % (value)

    def page(self, value):
        return '<textarea name="page" rows="20" cols="20" style="width:100%%">%s</textarea>' % (value)

    def version(self, value, view=0):
        return '<input type="text" name="version" size="10" maxlength="10" value="%s">' % (value)

    def pub_date(self, value, view=0):
        return '<input type=text name="pub_date" size="11" maxlength="10" value="%s">' % (value)

    def isbn(self, value, view=0):
        return '<input type=text name="isbn" size="13" maxlength="13" value="%s">' % (value)

    def encoding(self, value, view=0):
        if view==1:
            encoding = dms.encoding.get_by_id(value)
            if encoding:
                return encoding.encoding
            return ''
            
        combo = WOStringIO('<select name="encoding">\n')
        combo.write('<option></option>')
        encodings = dms.encoding.get_all()
        for key in encodings.sort_by('encoding'):
            encoding = encodings[key]
            combo.write("<option ")
            if encoding.encoding==value:
                combo.write("selected ")
            combo.write("value='" + encoding.encoding + "'>")
            combo.write(encoding.encoding)
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def initials(self, value, view=0):
        return '<input type=text name="initials" size="6" maxlength="5" value="%s">' % (value)

    def lint_time(self, value, view=0):
        return '<input type=text name="lint_time" size="11" maxlength="10" value="%s">' % (value)

    def mirror_time(self, value, view=0):
        return '<input type=text name="mirror_time" size="11" maxlength="10" value="%s">' % (value)

    def pub_time(self, value, view=0):
        return '<input type=text name="pub_time" size="11" maxlength="10" value="%s">' % (value)

    def title_compressed(self, value):
        """
        Compress the title so it will display well in 80 characters.
        Just add spaces around all + signs, which lets the title wrap.
        """
        
        parts = value.split('+')
        text = string.join(parts, ' + ')
        return text
        
    def headline(self, value):
        return '<input type=text name="headline" style="width:100%%" value="%s">' % value

    def short_title(self, value):
        return '<input type=text name="short_title" style="width:100%%" value="%s">' % value

    def menu_name(self, value):
        return '<input type=text name="menu_name" style="width:100%%" value="%s">' % escape_tokens(value)

    def short_desc(self, value):
        return '<input type=text name="short_desc" style="width:100%" value="' + value + '">'

    def last_update(self, value):
        return '<input type=text name="last_update" size="11"  maxlength="10" value="' + value + '">'

    def tickle_date(self, value):
        return '<input type=text name="tickle_date" size="11" maxlength="10" value="' + value + '">'

    def rating(self, value):
        return '<input type=text name="rating" size="2" maxlength="2" value="' + value + '">'

    def copyright_holder(self, value):
        return '<input type=text name="copyright_holder" size="20" value="' + value + '">'

    def tf(self, name, value, view=0):
        if view==1:
            if value==1:
                return '|stryes|'
            return '|strno|'

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

    def notes(self, value):
        return '<textarea name="notes" wrap="soft" rows="6" cols="10" style="width:100%">' + value + '</textarea>'
    
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
        return '<input type=text name="username" size="15" maxlength="40" value="%s">' % value

    def role_code(self, value, lang, view=0):
        if view==1:
            role = dms.role.get_by_id(value)
            if role:
                return role.name[lang]
            return ''

        combo = WOStringIO("<select name='role_code'>\n")
        roles = dms.role.get_all()
        for key in roles.sort_by_lang('name', lang):
            role = roles[key]
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
        collections = dms.collection.get_all()
        for key in collections.sort_by('sort_order'):
            collection = collections[key]
            assert not collection==None
            combo.write("<option ")
            if collection.code==value:
                combo.write("selected ")
            combo.write("value='%s'>%s</option>\n"
                        % (collection.code, collection.name[lang]))
        combo.write("</select>")
        return combo.get_value()

    def type_code(self, value, lang, view=0):
        if view==1:
            type = dms.type.get_by_id(value)
            if type:
                return type.name[lang]
            return ''

        combo = WOStringIO("<select name='type_code'>\n" \
                           "<option></option>\n")
        types = dms.type.get_all()
        for key in types.sort_by('sort_order'):
            type = types[key]
            combo.write("<option ")
            if type.code==value:
                combo.write("selected ")
            combo.write("value='%s'>%s</option>\n"
                        % (type.code, type.name[lang]))
        combo.write("</select>")
        return combo.get_value()

    def doc_id(self, value, lang):
        combo = WOStringIO("<select name='doc'>\n")
        docs = dms.document.get_all()
        for key in docs.sort_by('title'):
            doc = docs[key]
            if doc.lang==lang or lang==None:
                combo.write("<option ")
                if doc.id==value:
                    combo.write("selected ")
                combo.write("value='%s'>%s</option>\n"
                            % (str(doc.id), doc.title))
        combo.write("</select>")
        return combo.get_value()

    def sk_seriesid(self, value, view=0):
        if view==1:
            documents = dms.document.get_by_keys([['sk_seriesid', '=', value]])
            title = ''
            for key in documents.keys():
                doc = documents[key]
                if title > '':
                    title += '<br>'
                if doc.short_title > '':
                    title += doc.short_title
                else:
                    title += doc.title
            return title

        combo = WOStringIO('<select name="sk_seriesid">\n')
        combo.write('<option></option>\n')
        docs = dms.document.get_all()
        for key in docs.sort_by('title'):
            doc = docs[key]
            combo.write("<option ")
            if doc.sk_seriesid==value:
                combo.write("selected ")
            if doc.short_title > '':
                combo.write('value="%s">%s</option>\n'
                            % (str(doc.sk_seriesid), doc.short_title + ' (' + doc.lang + ')'))
            else:
                title = doc.title
                if title=='':
                    topfile = doc.top_file
                    if topfile:
                        title = topfile.title
                combo.write('value="%s">%s</option>\n'
                            % (str(doc.sk_seriesid), title[:40] + ' (' + doc.lang + ')'))
        combo.write("</select>\n")
        return combo.get_value()

    def replaced_by_id(self, value, view=0):
        docs = dms.document.get_all()
        if view==1:
            if docs.has_key(value):
                doc = docs[value]
                title = doc.title
                if title=='':
                    topfile = doc.top_file
                    if topfile:
                        title = topfile.title
                return title
            return ''

        combo = WOStringIO('<select name="replaced_by_id">\n')
        combo.write('<option></option>\n')
        for key in docs.sort_by('title'):
            doc = docs[key]
            combo.write("<option ")
            if doc.id==value:
                combo.write("selected ")
            if doc.short_title > '':
                combo.write("value='%s'>%s</option>\n"
                            % (str(doc.id),doc.short_title))
            else:
                title = doc.title
                if title=='':
                    topfile = doc.top_file
                    if topfile:
                        title = topfile.title
                combo.write("value='%s'>%s</option>\n"
                            % (str(doc.id), title[:40]))
        combo.write("</select>\n")
        return combo.get_value()

    def doc_lang(self, value, lang):
        combo = WOStringIO("<select name='lang'>\n")
        if value=='':
            combo.write('<option selected></option>')
        else:
            combo.write('<option></option>')
        languages = dms.language.get_all()
        for key in languages.sort_by_lang('name', lang):
            language = languages[key]
            if language.documents.count() > 0:
                combo.write("<option ")
                if language.code==value:
                    combo.write("selected ")
                combo.write("value='" + language.code + "'>")
                combo.write(language.name[lang])
                combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def new_page_lang(self, page_code, lang):
        combo = WOStringIO("<select name='lang'>\n")
        languages = dms.language.get_all()
        page = dms.page.get_by_id(page_code)
        for key in languages.sort_by_lang('name', lang):
            language = languages[key]
            if language.supported==1 and key not in page.title.keys():
                combo.write("<option value='" + language.code + "'>")
                combo.write(language.name[lang])
                combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def new_news_lang(self, news_id, lang):
        combo = WOStringIO("<select name='lang'>\n")
        languages = dms.language.get_all()
        news = dms.news.get_by_id(news_id)
        for key in languages.sort_by_lang('name', lang):
            language = languages[key]
            if language.supported==1 and key not in news.headline.keys():
                combo.write("<option value='" + language.code + "'>")
                combo.write(language.name[lang])
                combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def new_string_lang(self, string_code, lang):
        combo = WOStringIO("<select name='lang'>\n")
        languages = dms.language.get_all()
        webstring = dms.string.get_by_id(string_code)
        for key in languages.sort_by_lang('name', lang):
            language = languages[key]
            if language.supported==1 and key not in webstring.string.keys():
                combo.write("<option value='" + language.code + "'>")
                combo.write(language.name[lang])
                combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def lang(self, value, lang, allow_null=1, allow_unsupported=1, view=0):
        languages = dms.language.get_all()
        if view==1:
            if languages.has_key(value):
                language = languages[value]
                return language.name[lang]
            return ''

        combo = WOStringIO("<select name='lang'>\n")
        if allow_null==1:
            if value=='':
                combo.write('<option selected></option>')
            else:
                combo.write('<option></option>')
        for key in languages.sort_by_lang('name', lang):
            language = languages[key]
            if allow_unsupported==1 or language.supported==1:
                combo.write("<option ")
                if language.code==value:
                    combo.write("selected ")
                combo.write("value='" + language.code + "'>")
                combo.write(language.name[lang])
                combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def license_code(self, value, lang, view=0):
        if view==1:
            license = dms.license.get_by_id(value)
            if license:
                return license.name[lang]
            return ''

        combo = WOStringIO("<select name='license_code'>\n")
        combo.write('<option></option>')
        licenses = dms.license.get_all()
        for key in licenses.sort_by('sort_order'):
            license = licenses[key]
            assert not license==None
            combo.write("<option ")
            if license.code==value:
                combo.write("selected ")
            combo.write("value='" + license.code + "'>")
            combo.write(license.short_name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def license_version(self, value):
        return '<input type="text" name="license_version" value="' + value + '" size="10">'

    def page_code(self, value, lang):
        combo = WOStringIO("<select name='page_code'>\n")
        pages = dms.page.get_all()
        for key in pages.sort_by('page_code'):
            page = pages[key]
            assert not page==None
            combo.write("<option ")
            if page.code==value:
                combo.write("selected ")
            combo.write("value='" + str(page.code) + "'>")
            combo.write(page.title[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def pub_status_code(self, value, lang, view=0):
        if view==1:
            pubstatus = dms.pub_status.get_by_id(value)
            if pubstatus:
                return pubstatus.name[lang]
            return ''
            
        combo = WOStringIO("<select name='pub_status_code'>\n")
        combo.write('<option></option>')
        pub_statuses = dms.pub_status.get_all()
        for key in pub_statuses.sort_by('sort_order'):
            pubstatus = pub_statuses[key]
            assert not pubstatus==None
            combo.write("<option ")
            if pubstatus.code==value:
                combo.write("selected ")
            combo.write("value='" + pubstatus.code + "'>")
            combo.write(pubstatus.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()
        
    def review_status_code(self, value, lang, view=0):
        if view==1:
            status = dms.review_status.get_by_id(value)
            if status:
                return status.name[lang]
            return ''

        combo = WOStringIO("<select name='review_status_code'>\n")
        combo.write('<option></option>')
        review_statuses = dms.review_status.get_all()
        for key in review_statuses.sort_by('sort_order'):
            review_status = review_statuses[key]
            assert not review_status==None
            combo.write("<option ")
            if review_status.code==value:
                combo.write("selected ")
            combo.write("value='" + str(review_status.code) + "'>")
            combo.write(review_status.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def tech_review_status_code(self, value, lang, view=0):
        if view==1:
            status = dms.review_status.get_by_id(value)
            if status:
                return status.name[lang]
            return ''

        combo = WOStringIO("<select name='tech_review_status_code'>\n")
        combo.write('<option></option>')
        review_statuses = dms.review_status.get_all()
        for key in review_statuses.sort_by('sort_order'):
            review_status = review_statuses[key]
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
        topics = dms.topic.get_all()
        keys = topics.sort_by('sort_order')
        for key in keys:
            topic = topics[key]
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
            return octal2permission(value)
        else:
            return '|strunknown|'

    def section_code(self, value, lang):
        combo = WOStringIO('<select name="section_code">\n' \
                           '<option></option>\n')
        sections = dms.section.get_all()
        for key in sections.sort_by('sort_order'):
            section = sections[key]
            combo.write("<option ")
            if section.code==value:
                combo.write("selected ")
            combo.write("value='" + section.code + "'>")
            combo.write(section.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def template_code(self, value):
        combo = WOStringIO('<select name="template_code">\n')
        templates = dms.template.get_all()
        for key in templates.sort_by('code'):
            template = templates[key]
            combo.write("<option ")
            if template.code==value:
                combo.write("selected ")
            combo.write("value='" + template.code + "'>")
            combo.write(template.code)
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def data(self, value):
        return '<input type=text name="data" size="10"  maxlength="40" value="' + string.join(value) + '">'

    def sort_order(self, value):
        return '<input type=text name="sort_order" size="5" maxlength="5" value="' + str(value) + '">'

    def adjust_sort_order(self):
        return '<input type=text name="adjust_sort_order" size="5" maxlength="5" value="0">'

    def filename_compressed(self, value):
        """
        Compress the filename so it will display well in 80 characters.
        Just add spaces around all / slashes, which lets the filename wrap.
        """
        
        parts = value.split('/')
        text = string.join(parts, '/ ')
        text = text.replace('/ /', '//')
        text = text.replace('/ /', '//')
        return text

    def email(self, value):
        return '<input type="text" name="email" size="15" value="%s">' % value
        
    def delete(self):
        return '<input type="checkbox" name="delete">'

    def add(self):
        return '<input type="submit" name="add" value="|stradd|">'

    def save(self):
        return '<input type="submit" name="save" value="|strsave|">'

    def first_name(self, value):
        return '<input type=text name="first_name" size="12" value="%s">' % value

    def middle_name(self, value):
        return '<input type=text name="middle_name" size="12" value="%s">' % value

    def surname(self, value):
        return '<input type=text name="surname" size="12" value="%s">' % value

    def newpassword(self):
        return '<input type="text" name="password" size="12" value="">'

    def password(self, value):
        return '<input type="password" name="password" size="12" value="%s">' % value

    def string(self, value):
        return '<input type="text" name="webstring" size="30" value="%s" style="width:100%%">' % value

widgets = Widgets()
