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
Lampadas Session Manager Module

This module tracks users who have active sessions.
"""

# Modules

# FIXME import * is considered evil for you can pollute your namespace if
# the imported module changes or makes a mistake

from Globals import *
from BaseClasses import *
from Config import config
from Database import db
from Log import log


# Sessions

class Sessions(LampadasCollection):
    """
    All users with currently active sessions.
    """

    def __init__(self):
        self.load()

    def load(self):
        self.data = {}
        sql = 'SELECT username, ip_address, uri, timestamp FROM session'
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            session = Session()
            session.username   = trim(row[0])
            session.ip_address = trim(row[1])
            session.uri        = trim(row[2])
            session.timestamp  = time2str(row[3])
            self.data[session.username] = session
    
    def add(self, username, ip_address, uri=''):
        sql = 'INSERT INTO session(username, ip_address, uri) VALUES (' + wsq(username) + ', ' + wsq(ip_address) + ', ' + wsq(uri) + ')'
        db.runsql(sql)
        db.commit()
        session = Session(username)
        self.data[username] = session
        return session

    def delete(self, username):
        sql = 'DELETE FROM session WHERE username=' + wsq(username)
        db.runsql(sql)
        db.commit()
        del self[username]

    def count(self):
        return db.read_value('SELECT COUNT(*) FROM session')


class Session:

    def __init__(self, username=None):
        if username:
            sql = 'SELECT username, ip_address, uri, timestamp FROM session WHERE username=' + wsq(username)
            cursor = db.select(sql)
            row = cursor.fetchone()
            if row:
                self.username   = trim(row[0])
                self.ip_address = trim(row[1])
                self.uri        = trim(row[2])
                self.timestamp  = time2str(row[3])
                
    def refresh(self, ip_address, uri=''):
        sql = 'UPDATE session SET timestamp=now(), ip_address=' + wsq(ip_address) + ', uri=' + wsq(uri) + ' WHERE username=' + wsq(self.username)
        updated = db.runsql(sql)
        db.commit()
        if updated==0:
            log(3, self.username + '\'s session expired, recreating it.')
            sql = 'INSERT INTO session(username) VALUES (' + wsq(self.username) + ')'
            db.runsql(sql)
            db.commit()


sessions = Sessions()

# main
if __name__=='__main__' :
    print "Running unit tests..."
    print "End unit test run."
    
