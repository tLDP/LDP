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
Lampadas Database Module

This module generates a Database object for accessing a back-end RDBMS
"""

# Globals ##################################################################

AUTOCOMMIT = 1


# Modules ##################################################################

from Globals import *
from Config import config
import pyPgSQL
import os
import pwd
import types
import sys

class UnknownDBException(Exception):
    pass

class Database:
    """
    The database contains all users and documents
    """

    # FIXME : the python DB-API 2.0 states that you can transfer the burden
    # of quoting values to the cursor as in
    #
    # sql = "select * from document where doc_id = %(did)s"
    # param = {'did':'123'}
    # my_cursor.execute(sql,param)
    #
    # I like Python :-)
    #
    def execute(self, sql, params=None, log=1) :

        # FIXME: Log these commands as well as runsql. I'm getting errors, though -- maybe the % character?
        for k in params.keys():
            if type(params[k])==types.StringType:
                if params[k]=='':
                    params[k] = None
        
        cursor = self.connection.cursor()
        cursor.execute(sql,params)
        return cursor
    
    def select(self, sql):
        if config.log_sql:
            self.log(3, sql)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor

    def read_value(self, sql):
        if config.log_sql:
            self.log(3, sql)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        if row==None:
            value = None
        else:
            value = row[0]
        return value

    def max_id(self, table, field):
        if self.count(table)==0:
            return 0
        else:
            return self.read_value('SELECT MAX(' + field + ') FROM ' + table)
        
    def next_id(self, table, field):
        return self.max_id(table, field) + 1

    def runsql(self, sql, log=1):
        if config.log_sql and log==1:
            self.log(3, sql)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor.rowcount

    def count(self, table, whereclause=''):
        sql = 'SELECT COUNT(*) FROM ' + table
        if whereclause > '':
            sql = sql + ' WHERE ' + whereclause
        return int(self.read_value(sql))

    def log(self, level, message, username=''):
        if config.log_level >= level:
            sql = 'INSERT INTO log(level, username, message) VALUES (%s, %s, %s)' % (level, wsq(username), wsq(message))
            db.runsql(sql, log=0)
            db.commit()

    def commit(self):
        if AUTOCOMMIT==0:
            self.connection.commit()


# Specific derived DB classes ##################################################

class PgSQLDatabase(Database):

    def __init__(self, db_name, db_host):
        from pyPgSQL import PgSQL
	if len(db_host) == 0:
	    db_user = pwd.getpwuid(os.geteuid())[0]
            self.connection = PgSQL.connect(database=db_name, user=db_user)
        else:
            self.connection = PgSQL.connect(database=db_name, host=db_host)
        self.connection.autocommit = AUTOCOMMIT

class MySQLDatabase(Database):

    def __init__(self, db_name, db_host):
        from pyMySQL import MySQL
        self.connection = MySQL.connection(db_name=db_name)

def get_database(db_type, db_name, db_host):
    """
    Connect to the database specified in Config.

    See Factory Method design pattern.
    """
    if db_name=='':
        raise UnknownDBException('Database name not specified')
    elif db_type=='pgsql':
        db = PgSQLDatabase(db_name, db_host)
    elif db_type=='mysql':
        db = MySQLDatabase(db_name, db_host)
    else:
        raise UnknownDBException('Unknown database type %s, host is %s' % (db_type, db_host))
    return db

db = get_database(config.db_type, config.db_name, config.db_host)

