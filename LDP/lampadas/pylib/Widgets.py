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
from WebLayer import lampadasweb
from Languages import languages
import re
import string


class Widgets:
    """
    Generates low level widgets for use in constructing web pages. The use of
    the term "widget" is very loose since we also use this class to generate
    standard formats for some text items.
    """

    def format_code(self, value, lang, css_class='', view=0):
        if view==1:
            format = lampadas.formats[value]
            if format:
                return format.name[lang]
            return ''

        combo = WOStringIO('<select name="format_code"%s>\n' % css_class)
        combo.write('<option></option>')
        keys = lampadas.formats.sort_by_lang('name', lang)
        for key in keys:
            format = lampadas.formats[key]
            combo.write("<option ")
            if format.code==value:
                combo.write("selected ")
            combo.write("value='" + format.code + "'>")
            combo.write(format.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()
        
    def dtd_code(self, value, lang, css_class='', view=0):
        if view==1:
            dtd = lampadas.dtds[value]
            if dtd:
                return dtd.name[lang]
            return ''

        combo = WOStringIO('<select name="dtd_code"%s>\n' % css_class)
        if value=='':
            combo.write('<option selected></option>')
        else:
            combo.write('<option></option>')
        keys = lampadas.dtds.sort_by_lang('name', lang)
        for key in keys:
            dtd = lampadas.dtds[key]
            combo.write("<option ")
            if dtd.code==value:
                combo.write("selected ")
            combo.write("value='" + dtd.code + "'>")
            combo.write(dtd.name[lang])
            combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()
        
    def dtd_version(self, value, lang, css_class='', view=0):
        input = WOStringIO('<input type="text" name="dtd_version" size="8" maxlenth="20" value="%s"%s>' % (value, css_class))
        return input.get_value()

    def title(self, value, css_class='', view=0):
        return '<input type=text name="title" style="width:100%%" value="%s"%s>' % (escape_tokens(value), css_class)

    def abstract(self, value, css_class='', view=0):
        return '<textarea name="abstract" rows="6" cols="20" style="width:100%%"%s>%s</textarea>' % (css_class, value)

    def version(self, value, css_class='', view=0):
        return '<input type=text name="version" size="10" maxlength="10" value="%s"%s>' % (value, css_class)

    def pub_date(self, value, css_class='', view=0):
        return '<input type=text name="pub_date" size="11" maxlength="10" value="%s"%s>' % (value, css_class)

    def isbn(self, value, css_class='', view=0):
        return '<input type=text name="isbn" size="13" maxlength="13" value="%s"%s>' % (value, css_class)

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

    def stylesheet(self, value):
        return '<input type=text name="stylesheet" size="12" maxlength="12" value="%s">' % value
    
    def role_code(self, value, lang, view=0):
        if view==1:
            role = lampadas.roles[value]
            if role:
                return role.name[lang]
            return ''

        combo = WOStringIO("<select name='role_code'>\n")
        keys = lampadas.roles.sort_by_lang('name', lang)
        for key in keys:
            role = lampadas.roles[key]
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

    def type_code(self, value, lang, view=0):
        if view==1:
            type = lampadas.types[value]
            if type:
                return type.name[lang]
            return ''

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

    def sk_seriesid(self, value, view=0):
        if view==1:
            doc = lampadas.docs[value]
            if doc:
                return doc.title
            return ''

        combo = WOStringIO('<select name="sk_seriesid">\n')
        combo.write('<option></option>\n')
        keys = lampadas.docs.sort_by_metadata('title')
        for key in keys:
            doc = lampadas.docs[key]
            metadata = doc.metadata()
            combo.write("<option ")
            if doc.sk_seriesid==value:
                combo.write("selected ")
            if doc.short_title > '':
                combo.write("value='%s'>%s</option>\n"
                            % (str(doc.sk_seriesid), doc.short_title + ' (' + doc.lang + ')'))
            else:
                combo.write("value='%s'>%s</option>\n"
                            % (str(doc.sk_seriesid), metadata.title[:40] + ' (' + doc.lang + ')'))
        combo.write("</select>\n")
        return combo.get_value()

    def replaced_by_id(self, value, view=0):
        if view==1:
            doc = lampadas.docs[value]
            if doc:
                return doc.title
            return ''

        combo = WOStringIO('<select name="replaced_by_id">\n')
        combo.write('<option></option>\n')
        keys = lampadas.docs.sort_by('title')
        for key in keys:
            doc = lampadas.docs[key]
            metadata = doc.metadata()
            combo.write("<option ")
            if doc.id==value:
                combo.write("selected ")
            if doc.short_title > '':
                combo.write("value='%s'>%s</option>\n"
                            % (str(doc.id),doc.short_title))
            else:
                combo.write("value='%s'>%s</option>\n"
                            % (str(doc.id),metadata.title[:40]))
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

    def new_page_lang(self, page_code, lang):
        combo = WOStringIO("<select name='lang'>\n")
        page = lampadasweb.pages[page_code]
        keys = languages.sort_by_lang('name', lang)
        for key in keys:
            language = languages[key]
            assert not language==None
            if language.supported==1 and key not in page.title.keys():
                combo.write("<option value='" + language.code + "'>")
                combo.write(language.name[lang])
                combo.write("</option>\n")
        combo.write("</select>")
        return combo.get_value()

    def lang(self, value, lang, allow_null=1, allow_unsupported=1, view=0):
        if view==1:
            language = languages[value]
            if language:
                return language.name[lang]
            return ''

        combo = WOStringIO("<select name='lang'>\n")
        if allow_null==1:
            if value=='':
                combo.write('<option selected></option>')
            else:
                combo.write('<option></option>')
        keys = languages.sort_by_lang('name', lang)
        for key in keys:
            language = languages[key]
            assert not language==None
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
            license = lampadas.licenses[value]
            if license:
                return license.name[lang]
            return ''

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

    def license_version(self, value):
        return '<input type="text" name="license_version" value="' + value + '" size="10">'

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

    def pub_status_code(self, value, lang, view=0):
        if view==1:
            pubstatus = lampadas.pub_statuses[value]
            if pubstatus:
                return pubstatus.name[lang]
            return ''
            
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
        
    def review_status_code(self, value, lang, view=0):
        if view==1:
            status = lampadas.review_statuses[value]
            if status:
                return status.name[lang]
            return ''

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

    def tech_review_status_code(self, value, lang, view=0):
        if view==1:
            status = lampadas.review_statuses[value]
            if status:
                return status.name[lang]
            return ''

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
            return octal2permission(value)
        else:
            return '|strunknown|'

    def section_code(self, value, lang):
        combo = WOStringIO('<select name="section_code">\n' \
                           '<option></option>\n')
        section_codes = lampadasweb.sections.sort_by('sort_order')
        for section_code in section_codes:
            section = lampadasweb.sections[section_code]
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
        template_codes = lampadasweb.templates.sort_by('code')
        for template_code in template_codes:
            template = lampadasweb.templates[template_code]
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

widgets = Widgets()
