#!/usr/bin/python

"""
Interfaces to the database using enterprise.row.
"""

from Config import config
from twisted.enterprise import adbapi, row, reflector
from twisted.enterprise.sqlreflector import SQLReflector
from twisted.spread import pb
from twisted.internet import defer

class BlockRow(row.RowObject, pb.Referenceable):
    rowColumns = [('block_code', 'varchar'),
                  ('block',      'varchar'),
                  ('created',    'timestamp'),
                  ('updated',    'timestamp')]
    rowKeyColumns = [('block_code', 'varchar')]
    rowTableName = 'block'

class Block:

    def get_by_code(self, code):
        d = defer.Deferred()
        w = [('block_code', reflector.EQUAL, code)]
        refl.loadObjectsFrom('block', whereClause=w).addCallback(gotRows, d)
        return d
    
def gotRows(newRows, deferred):
    set = []
    for newrow in newRows:
        set.append(newrow)
    deferred.callback(set)

def runTests(result):
    print 'Done initializing'

if config.db_type=='pgsql':
    db_module = 'pyPgSQL.PgSQL'
else:
    db_module = 'pyMySQL.MySQL'

dbpool = adbapi.ConnectionPool(db_module, database=config.db_name, user='www-data')
refl = SQLReflector(dbpool, [BlockRow], runTests)
block = Block()

