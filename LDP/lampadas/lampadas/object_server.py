#!/usr/bin/python

from Config import config

from twisted.spread import pb
from twisted.internet import defer
from twisted.enterprise import adbapi, row, reflector
from twisted.enterprise.sqlreflector import SQLReflector

class BlockRow(row.RowObject, pb.Referenceable):
    rowColumns = [('block_code', 'varchar'),
                  ('block',      'varchar'),
                  ('created',    'timestamp'),
                  ('updated',    'timestamp')]
    rowKeyColumns = [('block_code', 'varchar')]
    rowTableName = 'block'

def connected(result):
    print 'Done initializing. Message: ', result

def success(object):
    print 'ObjectService loaded: ', object
    return object

class ObjectPerspective(pb.Perspective):

    def __init__(self, perspectiveName, identityName='Nobody'):
        pb.Perspective.__init__(self, perspectiveName, identityName)
        if config.db_type=='pgsql':
            db_module = 'pyPgSQL.PgSQL'
        else:
            db_module = 'pyMySQL.MySQL'
        dbpool = adbapi.ConnectionPool(db_module, database=config.db_name, user='www-data')
        self.reflector = SQLReflector(dbpool, [BlockRow], connected)

    def perspective_get_block_by_code(self, code):
        print 'ObjectService serving block: ', code
        w = [('block_code', reflector.EQUAL, code)]
        self.reflector.loadObjectsFrom('block', whereClause=w).addCallback(success)

class ObjectService(pb.Service):
    perspectiveClass = ObjectPerspective


