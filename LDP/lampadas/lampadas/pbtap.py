#!/usr/bin/python

import object_server
from twisted.python import usage
from twisted.spread import pb
from twisted.cred.authorizer import DefaultAuthorizer

class Options(usage.Options):
    optParameters = [["port", "o", 8790,
                      "Port to listen with ObjectService"]]
    
def updateApplication(app, config):
#    port = int(config["port"])
#    fact = pb.BrokerFactory(object_server.Block())
#    app.listenTCP(port, factory)

    # Test code, moving to use perspectives!
    port = config['port']
    if port:
        auth = DefaultAuthorizer(app)
        serv = object_server.ObjectService('lampadas.objects', app, auth)
        serv.createPerspective("guest").makeIdentity("guest")
        fact = pb.BrokerFactory(pb.AuthRoot(auth))
        app.listenTCP(int(port), fact)
    

#    appl = app.Application('pbsimple')
#    appl.listenTCP(8789, pb.BrokerFactory(Block()))
#    appl.run()
