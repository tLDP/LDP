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
from HTML import page_factory
from Log import log
from mod_python import apache
import os

def newdocument(req, username, doc_id,
             title, short_title,
             pub_status_code, type_code,
             version,
             review_status_code, tech_review_status_code,
             pub_date, last_update,
             tickle_date, isbn,
             format_code, dtd_code, dtd_version,
             lang, maintainer_wanted,
             license_code, license_version, copyright_holder,
             abstract, short_desc):

    # Generate a ScrollKeeper series ID
    command = 'scrollkeeper-gen-seriesid'
    process = os.popen(command)
    sk_seriesid = process.read()
    process.close()
    
    newdoc_id = lampadas.docs.add(title, short_title, type_code, format_code, dtd_code,
            dtd_version, version, last_update, isbn,
            pub_status_code, review_status_code, tickle_date, pub_date,
            tech_review_status_code, license_code, license_version,
            copyright_holder, abstract, short_desc, lang, sk_seriesid)

    # Add the current user as the author of the document
    doc = lampadas.docs[newdoc_id]
    doc.users.add(username)
    
    redirect(req, '/editdoc/' + str(newdoc_id) + referer_lang_ext(req))

def document(req, username, doc_id,
             title, short_title,
             pub_status_code, type_code,
             version,
             review_status_code, tech_review_status_code,
             pub_date, last_update,
             tickle_date, isbn,
             format_code, dtd_code, dtd_version,
             lang, maintainer_wanted,
             license_code, license_version, copyright_holder,
             abstract, short_desc, sk_seriesid):

    if not doc_id:
        return error("A required parameter is missing. Please go back and correct the error.")

    doc = lampadas.docs[int(doc_id)]
    if doc==None:
        return error("Cannot find document " + str(doc_id))

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
    doc.format_code             = format_code
    doc.dtd_code                = dtd_code
    doc.dtd_version             = dtd_version
    doc.lang                    = lang
    doc.abstract                = abstract
    doc.short_desc              = short_desc
    doc.sk_seriesid             = sk_seriesid
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
    
def newdocument_topic(req, doc_id, subtopic_code):
    doc = lampadas.docs[int(doc_id)]
    doc.topics.add(subtopic_code)
    go_back(req)
    
def deldocument_topic(req, doc_id, subtopic_code):
    doc = lampadas.docs[int(doc_id)]
    doc.topics.delete(subtopic_code)
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
        return page_factory.page('username_required')

    user = lampadas.users[username]
    if user:
        return page_factory.page('user_exists')
    if lampadas.users.is_email_taken(email):
        return page_factory.page('email_exists')

    password = random_string(12)
    send_mail(email, 'Your password for Lampadas is: ' + password)

    lampadas.users.add(username, first_name, middle_name, surname, email, 0, 0, password, '', 'default')
    return page_factory.page('account_created')

def newuser(req, username, email, first_name, middle_name, surname, stylesheet, password, admin, sysadmin, notes):
    """
    This routine is for when an administrator manually adds an account.
    """

    if username=='':
        return page_factory.page('username_required')

    user = lampadas.users[username]
    if user:
        return page_factory.page('user_exists')
    if lampadas.users.is_email_taken(email):
        return page_factory.page('email_exists')

    lampadas.users.add(username, first_name, middle_name, surname, email, int(admin), int(sysadmin), password, notes, stylesheet)
    redirect(req, '/user/' + username + referer_lang_ext(req))

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
    referer = req.headers_in['referer']
    req.headers_out['location'] = referer
    req.status = apache.HTTP_MOVED_TEMPORARILY

def mailpass(req, email):
    user = lampadas.users.find_email_user(email)
    if user:
        send_mail(email, 'Your password for Lampadas is: ' + user.password)
        redirect(req, '/password_mailed' + referer_lang_ext(req))
    else:
        return error('User not found.')

