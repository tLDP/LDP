#!/usr/bin/python

from twisted.spread import pb
from twisted.internet import defer
import database

class ObjectPerspective(pb.Perspective):

    def perspective_get_block_by_code(self, code):
        print 'ObjectService serving block: ', code
        d = defer.Deferred()
        database.block.get_by_code(code).addCallback(success, d)
        return d

def success(object, deferred):
    print 'ObjectService loaded: ', object
    deferred.callback(object)

class ObjectService(pb.Service):

    perspectiveClass = ObjectPerspective
        
