#!/usr/bin/python

"""
This is a test client, that requests a Perspective 
into the Lampadas Object Service.
"""

from twisted.python import log
log.discardLogs()
from twisted.internet import reactor
from twisted.spread import pb

def connected(perspective):
    print 'Connected.'
    perspective.callRemote('load').addCallbacks(success, failure)
    perspective.callRemote('page').addCallbacks(success, failure)

def connect_failure(error):
    print "Error connecting to ObjectService.."
    reactor.stop()

def success(block):
    print 'ObjectService gave me block: ' + block.code
    reactor.stop()

def failure(error):
    print "Failed to obtain a block from the ObjectService."
    reactor.stop()

def gotRoot(root):
    print 'Got root: ', root
    print dir(root)

def gotNoRoot(error):
    print 'Failed to obtain root: ', error

pb.connect("localhost", # host name
           8790, # port number
           "guest", # identity name
           "guest", # password
           "lampadas.objects", # service name
           "guest", # perspective name (usually same as identity)
           30 # timeout of 30 seconds before connection gives up
           ).addCallbacks(connected, # what to do when we get connected
                          connect_failure) # and what to do when we can't

pb.getObjectAt('localhost', 8790, 30).addCallbacks(gotRoot, gotNoRoot)
reactor.run() # start the main loop
