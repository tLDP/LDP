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
from Log import log
from mod_python import apache
import os
import string

from CoreDM import dms

# FIXME: Need permission checks on all of these routines!

def newdocument(req, username, doc_id,
             format_code, dtd_code, dtd_version,
             title, abstract, version,
             pub_date, isbn, encoding,
             short_title,
             pub_status_code, type_code,
             review_status_code, tech_review_status_code,
             last_update, tickle_date,
             lang, maintainer_wanted,
             license_code, license_version, copyright_holder,
             short_desc, replaced_by_id,
             lint_time, pub_time, mirror_time):

    sk_seriesid = new_sk_seriesid()
    
    doc = dms.document.new()
    doc.title = title
    doc.short_title = short_title
    doc.type_code = type_code
    doc.format_code = format_code
    doc.dtd_code = dtd_code
    doc.dtd_version = dtd_version
    doc.version = version
    doc.last_update = last_update
    doc.isbn = isbn
    doc.encoding = encoding
    doc.pub_status_code = pub_status_code
    doc.review_status_code = review_status_code
    doc.tickle_date = tickle_date
    doc.pub_date = pub_date
    doc.tech_review_status_code = tech_review_status_code
    doc.license_code = license_code
    doc.license_version = license_version
    doc.copyright_holder = copyright_holder
    doc.abstract = abstract
    doc.short_desc = short_desc
    doc.lang = lang
    doc.sk_seriesid = sk_seriesid
    doc.replaced_by_id = int('0' + replaced_by_id)
    doc.lint_time = lint_time
    doc.pub_time = pub_time
    doc.mirror_time = mirror_time
    dms.document.add(doc)

    # Add the current user as the author of the document
    docuser = dms.document_user.new()
    docuser.username = username
    docuser.doc_id = doc.id
    docuser.role_code='author'
    doc.users.add(docuser)
    
    redirect(req, '../../document_main/' + str(doc.id) + referer_lang_ext(req))

def document(req, username, doc_id,
             format_code, dtd_code, dtd_version,
             title, abstract, version,
             pub_date, isbn, encoding,
             short_title,
             pub_status_code, type_code,
             review_status_code, tech_review_status_code,
             last_update, tickle_date,
             lang, maintainer_wanted,
             license_code, license_version, copyright_holder,
             short_desc, sk_seriesid, replaced_by_id,
             lint_time, pub_time, mirror_time,
             delete=''):

    if not doc_id:
        return error("A required parameter is missing. Please go back and correct the error.")

    koc = dms.document.get_by_id(int(doc_id))
    if doc==None:
        return error("Cannot find document " + str(doc_id))

    if delete=='on':
        doc.delete()
        redirect(req, '../../document_deleted' + referer_lang_ext(req))
        return

    # Save all data to the document.
    doc.format_code             = format_code
    doc.dtd_code                = dtd_code
    doc.dtd_version             = dtd_version
    doc.title                   = title
    doc.abstract                = html_decode(abstract)
    doc.version                 = version
    doc.pub_date                = pub_date
    doc.isbn                    = isbn
    doc.encoding                = encoding
    doc.short_title             = short_title
    doc.pub_status_code         = pub_status_code
    doc.type_code               = type_code
    doc.review_status_code      = review_status_code
    doc.tech_review_status_code = tech_review_status_code
    doc.maintainer_wanted       = int(maintainer_wanted)
    doc.license_code            = license_code
    doc.license_version         = license_version
    doc.copyright_holder        = copyright_holder
    doc.last_update             = last_update
    doc.tickle_date             = tickle_date
    doc.lang                    = lang
    doc.short_desc              = short_desc
    doc.sk_seriesid             = sk_seriesid
    doc.replaced_by_id          = int('0' + replaced_by_id)
    doc.lint_time               = lint_time
    doc.pub_time                = pub_time
    doc.mirror_time             = mirror_time
    doc.save()
    go_back(req)

def newdocument_user(req, doc_id, username, active, role_code, email):
    user = dms.username.get_by_id(username)
    if user==None or user.username<>username:
        return error('User not found.')
    else:
        doc = dms.document.get_by_id(int(doc_id))
        docuser = dms.document_user.new()
        docuser.doc_id = doc.id
        docuser.username = username
        docuser.active = int(active)
        docuser.role_code = role_code
        docuser.email = email
        doc.users.add(docuser)
        go_back(req)
    
def document_user(req, doc_id, username, active, role_code, email, delete=''):
    doc = dms.document.get_by_id(int(doc_id))
    if delete=='on':
        doc.users.delete_by_keys([['username', '=', username]])
        go_back(req)
    else:
        docusers = doc.users.get_subset([['username', '=', username]])
        for key in docusers.keys():
            docuser = docusers[key]
            docuser.active = int(active)
            docuser.role_code = role_code
            docuser.email = email
            docuser.save()
        go_back(req)

# Note that data which is always read from the file directly,
# such as file size and permissions, are not part of the add
# interface, so we don't pass them.
def newdocument_file(req, doc_id, filename, top):
    doc = dms.document.get_by_id(int(doc_id))
    docfile = dms.document_file.new()
    docfile.doc_id = doc.id
    docfile.filename = filenaem
    docfile.top = int(top)
    doc.files.add(docfile)
    go_back(req)
    
def document_file(req, doc_id, filename, top, delete=''):
    doc = dms.document.get_by_id(int(doc_id))
    if delete=='on':
        doc.files.delete_by_keys([['filename', '=', filename]])
        go_back(req)
    else:
        docfiles = doc.files.get_subset([['filename', '=', filename]])
        for key in docfiles.keys():
            docfile = docfiles[key]
            docfile.top = int(top)
            file.save()
        go_back(req)
    
def newdocument_version(req, doc_id, version, pub_date, initials, notes):
    doc = dms.document.get_by_id(int(doc_id))
    docversion = dms.document_version.new()
    docversion.doc_id = doc.id
    docversion.version = version
    docversion.pub_date = pub_date
    docversion.initials = initials
    docversion.notes = notes
    doc.versions.add(docversion)
    go_back(req)
    
def document_version(req, rev_id, doc_id, version, pub_date, initials, notes, delete=''):
    doc = dms.document.get_by_id(int(doc_id))
    if delete=='on':
        doc.versions[int(rev_id)].delete()
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
    doc = dms.document.get_by_id(int(doc_id))
    doctopic = dms.document_topic.new()
    doctopic.doc_id = int(doc_id)
    doctopic.topic_code = topic_code
    doc.topics.add(doctopic)
    go_back(req)
    
def deldocument_topic(req, doc_id, topic_code):
    doc = dms.document.get_by_id(int(doc_id))
    doc.topics.delete_by_keys([['topic_code', '=', topic_code]])
    go_back(req)

def newdocument_note(req, doc_id, notes, creator):
    doc = dms.document.get_by_id(int(doc_id))
    docnote = dms.document_note.new()
    docnote.doc_id = doc.id
    docnote.creator = creator
    docnote.notes = notes
    doc.notes.add(docnote)
    go_back(req)
    
def newaccount(req, username, email, first_name, middle_name, surname):
    """
    This routine is for when a user requests an account.
    """
    
    if username=='':
        redirect(req, '../../username_required' + referer_lang_ext(req))

    user = dms.username.get_by_id(username)
    if user:
        redirect(req, '../../user_exists' + referer_lang_ext(req))
    
    email_users = dms.username.get_by_keys([['email', '=', email]])
    if email_users.count() > 0:
        redirect(req, '../../email_exists' + referer_lang_ext(req))

    password = random_string(12)
    user = dms.username.new()
    user.username = username
    user.first_name = first_name
    user.middle_name = middle_name
    user.surname = surname
    user.email = email
    user.password = password
    dms.username.add(user)

    send_mail(email, 'Your password for Lampadas is: ' + password)

    redirect(req, '../../account_created' + referer_lang_ext(req))

def newuser(req, username, email, first_name, middle_name, surname, password, admin, sysadmin, notes):
    """
    This routine is for when an administrator manually adds an account.
    """

    if username=='':
        redirect(req, '../../username_required' + referer_lang_ext(req))

    user = dms.username.get_by_id(username)
    if user:
        redirect(req, '../../user_exists' + referer_lang_ext(req))
    
    email_users = dms.username.get_by_keys([['email', '=', email]])
    if email_users.count() > 0:
        redirect(req, '../../email_exists' + referer_lang_ext(req))

    user = dms.username.new()
    user.username = username
    user.first_name = first_name
    user.middle_name = middle_name
    user.surname = surname
    user.email = email
    user.password = password
    user.admin = int(admin)
    user.sysadmin = int(sysadmin)
    user.notes = notes
    dms.username.add(user)

    redirect(req, '../../user/' + username + referer_lang_ext(req))

def user(req, username, first_name, middle_name, surname, email, password, admin, sysadmin, notes):
    user = dms.username.get_by_id(username)
    if not user==None:
        user.first_name = first_name
        user.middle_name = middle_name
        user.surname = surname
        user.email = email
        if password > '':
            user.password = password
        user.admin = int(admin)
        user.sysadmin = int(sysadmin)
        user.notes = notes
        user.save()
    go_back(req)

def newnews(req, pub_date):
    newsitem = dms.news.new()
    newsitem.pub_date = pub_date
    dms.news.add(newsitem)
    redirect(req, '../../news_edit/' + str(newsitem.id) + referer_lang_ext(req))

def news(req, news_id, pub_date):
    newsitem = dms.news.get_by_id(int(news_id))
    newsitem.pub_date = pub_date
    newsitem.save()
    go_back(req)

def news_lang(req, news_id, lang, headline, news, version):
    newsitemi18ns = dms.news_i18n.get_by_keys([['news_id', '=', int(news_id)], ['lang', '=', lang]])
    newsitemi18n = newsitemi18ns[newsitemi18ns.keys()[0]]
    newsitemi18n.headline[lang] = headline
    newsitemi18n.news[lang] = news
    newsitemi18n.version[lang] = version
    newsitemi18n.save()
    go_back(req)

def newnews_lang(req, news_id, lang, headline, news, version):
    newsitem = dms.news_i18n.new()
    newsitem.id = int(news_id)
    newsitem.lang = lang
    newsitem.headline = headline
    newsitem.news = news
    newsitem.version = version
    dms.news.add(newsitem)
    go_back(req)

def newpage(req, page_code, section_code, template_code,
            only_dynamic, only_registered, only_admin, only_sysadmin, data):
    page = dms.page.new()
    page.code = page_code
    page.section_code = section_code
    page.template_code = template_code
    page.only_dynamic = int(only_dynamic)
    page.only_registered = int(only_registered)
    page.only_admin = int(only_admin)
    page.only_sysadmin = int(only_sysadmin)
    page.data = data
    dms.page.add(page)
    redirect(req, '../../page_edit/' + str(page.code) + referer_lang_ext(req))

def page(req, page_code, section_code, template_code,
            only_dynamic, only_registered, only_admin, only_sysadmin, data, adjust_sort_order):
    page = dms.page.get_by_id(page_code)
    page.section_code = section_code
    page.template_code = template_code
    page.only_dynamic = int(only_dynamic)
    page.only_registered = int(only_registered)
    page.only_admin = int(only_admin)
    page.only_sysadmin = int(only_sysadmin)
    page.data = string.split(data, ' ')
#    lampadasweb.pages.adjust_sort_order(page.code, int(adjust_sort_order))
    page.save()
    go_back(req)

def page_lang(req, page_code, lang, title, menu_name, page, version):
    pagei18ns = dms.page_i18n.get_by_keys([['page_code', '=', page_code], ['lang', '=', lang]])
    pagei18n = pagei18ns[pagei18ns.keys()[0]]
    pagei18n.title = title
    pagei18n.menu_name = menu_name
    pagei18n.page = page
    pagei18n.version = version
    pagei18n.save()
    go_back(req)

def newpage_lang(req, page_code, lang, title, menu_name, page, version):
    pagei18n = dms.page_i18n.new()
    pagei18n.code = page_code
    pagei18n.lang = lang
    pagei18n.title = title
    pagei18n.menu_name = menu_name
    pagei18n.page = page
    pagei18n.version = version
    dms.page_i18n.add(page_i18n)
    go_back(req)

def newstring(req, string_code):
    webstring = dms.webstring.new()
    webstring.code = string_code
    dms.webstring.add(webstring)
    redirect(req, '../../string_edit/' + str(webstring.code) + referer_lang_ext(req))

def string_lang(req, string_code, lang, webstring, version):
    webstringi18ns = dms.webstring_i18n.get_by_keys([['string_code', '=', string_code], ['lang', '=', lang]])
    webstringi18n = webstringi18ns[webstringi18ns.keys()[0]]
    webstringi18n.string = webstring
    webstringi18n.version = version
    dms.webstring_i18n.add(webstringi18n)
    go_back(req)

def newstring_lang(req, string_code, lang, webstring, version):
    webstringi18n = dms.webstring_i18n.new()
    webstringi18n.code = string_code
    webstringi18n.lang = lang
    webstringi18n.string = webstring
    webstringi18n.version = version
    dms.webstring_i18n.add(webstringi18n)
    go_back(req)
