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
Lampadas Object Hierarchy Module

This module defines Data Objects (Users, Docs, Notes, Topics, etc.)
for the Lampadas system. All access to the underlying database should be
performed through this layer.
"""

# Modules

from Globals import *
from Config import config
from Database import db
from Log import log
from BaseClasses import *
from SourceFiles import sourcefiles
from ErrorTypes import errortypes
from Errors import errors
from Languages import languages
from DocTopics import doctopics, DocTopics
from Encodings import encodings, Encodings
from Types import types, Types
from Roles import roles, Roles
from Licenses import licenses, Licenses
from DTDs import dtds, DTDs
from Formats import formats, Formats
from PubStatuses import pub_statuses, PubStatuses
from ReviewStatuses import review_statuses, ReviewStatuses
from Topics import topics, Topics
from Collections import collections, Collections
import string
import os.path


# UserDocs

class UserDocs(LampadasCollection):
    """
    A collection object providing access to all user document associations.
    """

    def __init__(self, username):
        self.data = {}
        self.username = username
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT doc_id, username, role_code, email, active FROM document_user WHERE username=" + wsq(username)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            newUserDoc = UserDoc()
            newUserDoc.load_row(row)
            self.data[newUserDoc.doc_id] = newUserDoc


    def add(self, doc_id, role_code, email, active):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "INSERT INTO document_user(doc_id, username, role_code, email, active) VALUES (" + str(doc_id) + ", " + wsq(self.username) + ", " + wsq(role_code) + ", " + wsq(email) + ", " + wsq(bool2tf(active)) +  " )"
        assert db.runsql(sql)==1
        db.commit()
        newUserDoc = UserDoc()
        self.data[doc_id] = newUserDoc
    
    def delete(self, doc_id):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = 'DELETE from document_user WHERE doc_id=' + str(doc_id) + ' AND username=' + wsq(self.username)
        assert db.runsql(sql)==1
        db.commit()
        del self.data[doc_id]

class UserDoc:
    """
    An association between a user and a document. This association defines the role
    which the user plays in the production of the document.
    """

    def load_row(self, row):
        self.doc_id		= row[0]
        self.username	= trim(row[1])
        self.role		= trim(row[2])
        self.email		= trim(row[3])
        self.active		= tf2bool(row[4])

    def save(self):
        """
        FIXME: use cursor.execute(sql,params) instead! --nico
        """
        sql = "UPDATE document_user SET role=" + wsq(self.role) + ", email=" + wsq(self.email) + ", active=" + wsq(bool2tf(self.active)) + " WHERE doc_id=" + str(self.doc_id) + " AND username=" + wsq(self.username)
        db.runsql(sql)
        db.commit()


# Users

class Users:
    """
    A collection object providing access to registered users.
    """

    def __getitem__(self, username):
        user = User(username)
        if user.username==username:
            return User(username)
        else:
            return None

    def count(self):
        return db.read_value('SELECT count(*) from username')

    def add(self, username, first_name, middle_name, surname, email, admin, sysadmin, password, notes):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "INSERT INTO username (username, first_name, middle_name, surname, email, admin, sysadmin, password, notes) VALUES (" + wsq(username) + ", " + wsq(first_name) + ", " + wsq(middle_name) + ", " + wsq(surname) + ", " + wsq(email) + ", " + wsq(bool2tf(admin)) + ", " + wsq(bool2tf(sysadmin)) + ", " + wsq(password) + ", " + wsq(notes) + ")"
        assert db.runsql(sql)==1
        db.commit()
        user = self[username]
        return user
    
    def delete(self, username):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = 'DELETE from username WHERE username=' + wsq(username)
        assert db.runsql(sql)==1
        db.commit()

    def is_email_taken(self, email):
        value = db.read_value('SELECT COUNT(*) FROM username WHERE email=' + wsq(email))
        return value

    def find_session_user(self, session_id):
        """
        Looks a session_id up in the username table, to see which user owns the session.
        """

        log(3, 'looking for user session: ' + session_id)
        if session_id > '':
        # FIXME: use cursor.execute(sql,params) instead! --nico
            sql = 'SELECT username FROM username WHERE session_id=' + wsq(session_id)
            cursor = db.select(sql)
            row = cursor.fetchone()
            if row:
                log(3, 'found user session: ' + row[0])
                return trim(row[0])
        return ''

    def find_email_user(self, email):
        sql = 'SELECT username FROM username WHERE email=' + wsq(email)
        cursor = db.select(sql)
        row = cursor.fetchone()
        if row:
            username = trim(row[0])
            user = self[username]
            return user
        
    def letter_keys(self, letter):
        keys = []
        sql = 'SELECT username FROM username WHERE upper(substr(username,1,1))=' + wsq(letter.upper())
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            username = trim(row[0])
            keys = keys + [username]
        keys.sort()
        return keys
        
class User:
    """
    A user who is known by the system can login to manipulate documents
    and act on the database according to his rights.
    """

    def __init__(self, username='') :
        self.username       = ''
        self.session_id     = ''
        self.first_name     = ''
        self.middle_name    = ''
        self.surname        = ''
        self.email          = ''
        self.admin          = 0
        self.sysadmin       = 0
        self.password       = ''
        self.notes          = ''
        self.name           = ''

        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = 'SELECT username, session_id, first_name, middle_name, surname, email, admin, sysadmin, password, notes FROM username WHERE username=' + wsq(username)
        cursor = db.select(sql)
        row = cursor.fetchone()
        if row==None:
            return
        self.username       = trim(row[0])
        self.session_id     = trim(row[1])
        self.first_name     = trim(row[2])
        self.middle_name    = trim(row[3])
        self.surname        = trim(row[4])
        self.email          = trim(row[5])
        self.admin          = tf2bool(row[6])
        self.sysadmin       = tf2bool(row[7])
        self.password       = trim(row[8])
        self.notes          = trim(row[9])
        self.name           = trim(trim(self.first_name + ' ' + self.middle_name) + ' ' + self.surname)

        self.docs = UserDocs(self.username)

    def save(self):
        """
        FIXME: use cursor.execute(sql,params) instead! --nico
        """
        sql = 'UPDATE username SET session_id=' + wsq(self.session_id) + ', first_name=' + wsq(self.first_name) + ', middle_name=' + wsq(self.middle_name) + ', surname=' + wsq(self.surname) + ', email=' + wsq(self.email) + ', admin=' + wsq(bool2tf(self.admin)) + ', sysadmin=' + wsq(bool2tf(self.sysadmin)) + ', password=' + wsq(self.password) + ', notes=' + wsq(self.notes) + ' WHERE username=' + wsq(self.username)
        db.runsql(sql)
        db.commit()

    def can_edit(self, doc_id=None, username=None, news_id=None, page_code=None, string_code=None):

        # Sysadmin can do anything
        if self.sysadmin > 0:
            return 1

        if not doc_id==None:
            if self.docs.has_key(doc_id):
                return 1
            if self.admin==1:
                return 1
            if doc_id==0:
                return config.user_can_add_doc
                    
        if not page_code==None:
            if self.admin==1:
                if page_code=='':
                    return config.admin_can_add_page
                else:
                    return config.admin_can_edit_page
                
        if not string_code==None:
            if self.admin==1:
                if string_code=='':
                    return config.admin_can_add_string
                else:
                    return config.admin_can_edit_string

        if not username==None:
            if username==self.username:
                return 1
            elif self.admin==1:
                if user_code=='':
                    return config.admin_can_add_user
                else:
                    return config.admin_can_edit_user

        return 0

users = Users()


# main
if __name__=='__main__' :
    pass
