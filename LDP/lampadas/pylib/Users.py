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

from Globals import *
from Config import config
from Database import db
from Log import log
from BaseClasses import *
from DocUsers import docusers, DocUsers

class Users(DataCollection):
    """
    A collection object providing access to registered users.
    """

    def __init__(self):
        DataCollection.__init__(self, None, User,
                               'username',
                               {'username':     {'data_type': 'string'}},
                               [{'session_id':  {'data_type': 'string'}},
                                {'first_name':  {'data_type': 'string'}},
                                {'middle_name': {'data_type': 'string'}},
                                {'surname':     {'data_type': 'string'}},
                                {'email':       {'data_type': 'string'}},
                                {'admin':       {'data_type': 'bool'}},
                                {'sysadmin':    {'data_type': 'bool'}},
                                {'password':    {'data_type': 'string'}},
                                {'notes':       {'data_type': 'string'}},
                                {'created':     {'data_type': 'created'}},
                                {'updated':     {'data_type': 'updated'}}],
                               [],
                               cache_size=100)

    def is_email_taken(self, email):
        value = db.read_value('SELECT COUNT(*) FROM username WHERE email=' + wsq(email))
        return value

    def find_session_user(self, session_id):
        """
        Looks a session_id up in the username table, to see which user owns the session.
        """

        log(3, 'looking for user session: ' + session_id)
        if session_id > '':
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
        
class User(DataObject):
    """
    A user who is known by the system can login to manipulate documents
    and act on the database according to his rights.
    """

    def __init__(self, parent) :
        DataObject.__init__(self, parent)
        DataObject.add_child(self, 'docs', docusers.apply_filter(DocUsers, Filter(self, 'username', '=', 'username')))

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
