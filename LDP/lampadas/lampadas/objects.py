#!/usr/bin/python

# Lampadas imports
from Config import config

# Twisted imports
from twisted.internet import reactor
from twisted.enterprise import adbapi, row, reflector
from twisted.enterprise.sqlreflector import SQLReflector
from twisted.python import usage
from twisted.cred.authorizer import DefaultAuthorizer
from twisted.internet import defer

# Sibling imports
from row import BlockRow, PageRow, PageI18nRow

ROW_CLASSES = [BlockRow, PageRow, PageI18nRow]

class Page:
    def __init__(self, refl):
        self.refl = refl

    def get_all(self, callback):
        print 'Page.get_all()'
        self.refl.loadObjectsFrom('page').addCallback(callback)

    def get_by_code(self, code, callback):
        print 'Page.get_by_code(%s): ' % code
        w = [('block_code', reflector.EQUAL, code)]
        self.refl.loadObjectsFrom('block', whereClause=w).addCallback(callback)

class Objects:
    def connect(self, callback):
        if config.db_type=='pgsql':
            db_module = 'pyPgSQL.PgSQL'
        else:
            db_module = 'pyMySQL.MySQL'
        self.dbpool = adbapi.ConnectionPool(db_module, database=config.db_name, user='www-data')
        self.refl = SQLReflector(self.dbpool, ROW_CLASSES, callback)
        self.page = Page(self.refl)

object_server = Objects()
