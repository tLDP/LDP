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

from Globals import *
from globals import *
from Config import config
from DataLayer import lampadas
from WebLayer import lampadasweb
from Log import log
from mod_python import apache
import os
import string


# FIXME: Need permission checks on all of these routines!

def newdocument(req, username, doc_id,
             title, short_title,
             pub_status_code, type_code,
             version,
             review_status_code, tech_review_status_code,
             pub_date, last_update,
             lint_time, pub_time, mirror_time,
             tickle_date, isbn,
             lang, maintainer_wanted,
             license_code, license_version, copyright_holder,
             abstract, short_desc, replaced_by_id):

    sk_seriesid = new_sk_seriesid()
    
    doc = lampadas.docs.add(title, short_title, type_code,
          '', '', '',
          version, last_update, isbn,
          pub_status_code, review_status_code, tickle_date, pub_date,
          tech_review_status_code, license_code, license_version,
          copyright_holder, abstract, short_desc, lang, sk_seriesid,
          int('0' + replaced_by_id),
          lint_time, pub_time, mirror_time)

    # Add the current user as the author of the document
    doc.users.add(username)
    
    redirect(req, '../../document_main/' + str(doc.id) + referer_lang_ext(req))

def document(req, username, doc_id,
             title, short_title,
             pub_status_code, type_code,
             version,
             review_status_code, tech_review_status_code,
             pub_date, last_update,
             tickle_date, isbn,
             lang, maintainer_wanted,
             license_code, license_version, copyright_holder,
             abstract, short_desc, sk_seriesid, replaced_by_id,
             lint_time, pub_time, mirror_time):

    if not doc_id:
        return error("A required parameter is missing. Please go back and correct the error.")

    doc = lampadas.docs[int(doc_id)]
    if doc==None:
        return error("Cannot find document " + str(doc_id))

    # Save all data to the document.
    doc.title                   = title
    doc.short_title             = short_title
    doc.pub_status_code         = pub_status_code
    doc.type_code               = type_code
    doc.review_status_code      = review_status_code
    doc.tech_review_status_code = tech_review_status_code
    doc.maintainer_wanted       = int(maintainer_wanted)
    doc.license_code            = license_code
    doc.license_version         = license_version
    doc.copyright_holder        = copyright_holder
    doc.pub_date                = pub_date
    doc.last_update             = last_update
    doc.version                 = version
    doc.tickle_date             = tickle_date
    doc.ibsn                    = isbn
    doc.lang                    = lang
    doc.abstract                = abstract
    doc.short_desc              = short_desc
    doc.sk_seriesid             = sk_seriesid
    doc.replaced_by_id          = int('0' + replaced_by_id)
    doc.lint_time               = lint_time
    doc.pub_time                = pub_time
    doc.mirror_time             = mirror_time
    doc.save()
    go_back(req)

def newdocument_user(req, doc_id, username, active, role_code, email, action):
    user = lampadas.users[username]
    if user==None or user.username<>username:
        return error('User not found.')
    else:
        doc = lampadas.docs[int(doc_id)]
        doc.users.add(username, role_code, email, int(active))
        go_back(req)
    
def document_user(req, doc_id, username, active, role_code, email, action, delete=''):
    doc = lampadas.docs[int(doc_id)]
    if delete=='on':
        doc.users.delete(username)
        go_back(req)
    else:
        docuser = doc.users[username]
        docuser.active = int(active)
        docuser.role_code = role_code
        docuser.email = email
        docuser.save()
        go_back(req)

# Note that data which is always read from the file directly,
# such as file size and permissions, are not part of the add
# interface, so we don't pass them.
def newdocument_file(req, doc_id, filename, top):
    doc = lampadas.docs[int(doc_id)]
    doc.files.add(doc_id, filename, int(top))
    go_back(req)
    
def document_file(req, doc_id, filename, top, action, delete=''):
    doc = lampadas.docs[int(doc_id)]
    if delete=='on':
        doc.files.delete(filename)
        go_back(req)
    else:
        file = doc.files[filename]
        file.top = int(top)
        file.save()
        go_back(req)
    
def newdocument_version(req, doc_id, version, pub_date, initials, notes, action):
    doc = lampadas.docs[int(doc_id)]
    doc.versions.add(version, pub_date, initials, notes)
    go_back(req)
    
def document_version(req, rev_id, doc_id, version, pub_date, initials, notes, action, delete=''):
    doc = lampadas.docs[int(doc_id)]
    if delete=='on':
        doc.versions.delete(int(rev_id))
        go_back(req)
    else:
        docversion = doc.versions[int(rev_id)]
        docversion.version = version
        docversion.pub_date = pub_date
        docversion.initials = initials
        docversion.notes = notes
        docversion.save()
        go_back(req)
    
def newdocument_topic(req, doc_id, topic_code):
    doc = lampadas.docs[int(doc_id)]
    doc.topics.add(topic_code)
    go_back(req)
    
def deldocument_topic(req, doc_id, topic_code):
    doc = lampadas.docs[int(doc_id)]
    doc.topics.delete(topic_code)
    go_back(req)

def newdocument_note(req, doc_id, notes, creator):
    doc = lampadas.docs[int(doc_id)]
    doc.notes.add(notes, creator)
    go_back(req)
    
def newaccount(req, username, email, first_name, middle_name, surname):
    """
    This routine is for when a user requests an account.
    """
    
    if username=='':
        redirect(req, '../../username_required' + referer_lang_ext(req))

    user = lampadas.users[username]
    if user:
        redirect(req, '../../user_exists' + referer_lang_ext(req))
    if lampadas.users.is_email_taken(email):
        redirect(req, '../../email_exists' + referer_lang_ext(req))

    password = random_string(12)
    send_mail(email, 'Your password for Lampadas is: ' + password)

    lampadas.users.add(username, first_name, middle_name, surname, email, 0, 0, password, '', 'default')
    redirect(req, '../../account_created' + referer_lang_ext(req))

def newuser(req, username, email, first_name, middle_name, surname, stylesheet, password, admin, sysadmin, notes):
    """
    This routine is for when an administrator manually adds an account.
    """

    if username=='':
        redirect(req, '../../username_required' + referer_lang_ext(req))

    user = lampadas.users[username]
    if user:
        redirect(req, '../../user_exists' + referer_lang_ext(req))
    if lampadas.users.is_email_taken(email):
        redirect(req, '../../email_exists' + referer_lang_ext(req))

    lampadas.users.add(username, first_name, middle_name, surname, email, int(admin), int(sysadmin), password, notes, stylesheet)
    redirect(req, '../../user/' + username + referer_lang_ext(req))

def user(req, username, first_name, middle_name, surname, email, stylesheet, password, admin, sysadmin, notes):
    user = lampadas.users[username]
    if not user==None:
        user.first_name = first_name
        user.middle_name = middle_name
        user.surname = surname
        user.email = email
        user.stylesheet = stylesheet
        if password > '':
            user.password = password
        user.admin = int(admin)
        user.sysadmin = int(sysadmin)
        user.notes = notes
        user.save()
    go_back(req)

def newnews(req, pub_date):
    newsitem = lampadasweb.news.add(pub_date)
    redirect(req, '../../news_edit/' + str(newsitem.id) + referer_lang_ext(req))

def news(req, news_id, pub_date):
    newsitem = lampadasweb.news[int(news_id)]
    newsitem.pub_date = pub_date
    newsitem.save()
    go_back(req)

def news_lang(req, news_id, lang, news):
    newsitem = lampadasweb.news[int(news_id)]
    newsitem.news[lang] = news
    newsitem.save()
    go_back(req)

def newnews_lang(req, news_id, lang, news):
    newsitem = lampadasweb.news[int(news_id)]
    newsitem.add_lang(lang, news)
    go_back(req)

def newpage(req, page_code, sort_order, section_code, template_code,
            only_dynamic, only_registered, only_admin, only_sysadmin, data):
    page = lampadasweb.pages.add(page_code, int(sort_order), section_code, template_code, int(only_dynamic), int(only_registered), int(only_admin), int(only_sysadmin), string.split(data, ' '))
    redirect(req, '../../page_edit/' + str(page.code) + referer_lang_ext(req))

def page(req, page_code, sort_order, section_code, template_code,
            only_dynamic, only_registered, only_admin, only_sysadmin, data, adjust_sort_order):
    page = lampadasweb.pages[page_code]
    page.sort_order   = int(sort_order)
    page.section_code = section_code
    page.template_code = template_code
    page.only_dynamic = int(only_dynamic)
    page.only_registered = int(only_registered)
    page.only_admin = int(only_admin)
    page.only_sysadmin = int(only_sysadmin)
    page.data = string.split(data, ' ')
    lampadasweb.pages.adjust_sort_order(page.code, int(adjust_sort_order))
    page.save()
    go_back(req)

def page_lang(req, page_code, lang, title, menu_name, page, version):
    webpage = lampadasweb.pages[page_code]
    webpage.title[lang] = title
    webpage.menu_name[lang] = menu_name
    webpage.page[lang] = page
    webpage.version[lang] = version
    webpage.save()
    go_back(req)

def newpage_lang(req, page_code, lang, title, menu_name, page, version):
    webpage = lampadasweb.pages[page_code]
    webpage.add_lang(lang, title, menu_name, page, version)
    go_back(req)

def newstring(req, string_code):
    astring = lampadasweb.strings.add(string_code)
    redirect(req, '../../string_edit/' + str(astring.code) + referer_lang_ext(req))

def string_lang(req, string_code, lang, string):
    astring = lampadasweb.strings[string_code]
    astring.string[lang] = string
    astring.save()
    go_back(req)

def newstring_lang(req, string_code, lang, string):
    astring = lampadasweb.strings[string_code]
    astring.add_lang(lang, string)
    go_back(req)
