#!/usr/bin/python

# Lampadas imports
from Config import config

# Twisted imports
from twisted.spread import pb
from twisted.internet import reactor
from twisted.enterprise import adbapi, row, reflector
from twisted.enterprise.sqlreflector import SQLReflector
from twisted.python import usage
from twisted.cred.authorizer import DefaultAuthorizer
from twisted.internet import defer

# Sibling imports
from row import BlockRow, PageRow, PageI18nRow

ROW_CLASSES = [BlockRow, PageRow, PageI18nRow]

def loaded(object):
    print 'ObjectService loaded: ', object
    return object

class Page(pb.Copyable):
    def __init__(self, refl):
        print 'Initializing Page'
        refl.loadObjectsFrom('page').addCallback(self.loaded)
    
    def loaded(self, pages):
        print 'Page.loaded()'
        self.pages = pages
        
    def get_all(self, refl):
        refl.loadObjectsFrom('page').addCallback(loaded)

    def get_by_code(self, refl, code):
        print 'ObjectService serving block: ', code
        w = [('block_code', reflector.EQUAL, code)]
        refl.loadObjectsFrom('block', whereClause=w).addCallback(loaded)

def connected(result):
    print 'Object Server Ready.'

class Objects(pb.Perspective):
    
    def __init__(self, perspectiveName, identityName='Nobody'):
        pb.Perspective.__init__(self, perspectiveName, identityName)
        if config.db_type=='pgsql':
            self.db_module = 'pyPgSQL.PgSQL'
        else:
            self.db_module = 'pyMySQL.MySQL'
        self.dbpool = adbapi.ConnectionPool(self.db_module, database=config.db_name, user='www-data')
        self.refl = SQLReflector(self.dbpool, ROW_CLASSES, connected)
        reactor.callLater(0.5, self.load)

    def load(self):
        print 'Objects.load()'
        self.page = Page(self.refl)

    def perspective_page(self):
        print 'Client requested pages'
        return self.page.pages

class ObjectService(pb.Service):
    perspectiveClass = Objects


class Options(usage.Options):
    optParameters = [['port', 'p', 8790, 'Port to listed on.']]

def updateApplication(app, config):
    port = config['port']
    if port:
        auth = DefaultAuthorizer(app)
        serv = ObjectService('lampadas.objects', app, auth)
        serv.createPerspective("guest").makeIdentity("guest")
        fact = pb.BrokerFactory(pb.AuthRoot(auth))
        app.listenTCP(int(port), fact)
    reactor.run()
    
