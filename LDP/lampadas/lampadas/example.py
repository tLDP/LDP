#!/usr/bin/python

from twisted.internet import app
from twisted.python import usage, components
from twisted.web.resource import Resource
from twisted.internet import reactor

from twisted.web.woven import model, view, controller, interfaces
from twisted.web.woven import widgets
from twisted.web import domhelpers, server
import twisted.web
import twisted.protocols.http

class MList(model.ListModel):
    def __init__(self, orig, *args, **kwargs):
        print 'Initializing...'
        model.Model.__init__(self, *args, **kwargs)
        model.ListModel.__init__(self, orig)

class VList(view.WView):
    templateFile = 'example.xhtml'

    #def setUp(self, request, document):
        #print 'Initializing List View: '

    def wvfactory_list(self, request, node, model):
        #domhelpers.clearNode(node)
        return widgets.List(model)
    
class CList(controller.WController):
    pass

view.registerViewForModel(VList, MList)
controller.registerControllerForModel(CList, MList)


class Options(usage.Options):
    optParameters = [["port", "p", 8080,
                      "Port to listen with Webserver"]]
    
class Page(twisted.web.widgets.WidgetPage):
    template = '<html><head></head><body>%%%%self.widget%%%%</body></html>'

class Foo:
    pass

foo = Foo()
foo.list = ['foo', 'bar']

class Gadget(twisted.web.widgets.Gadget):
    def __init__(self):
        print 'Initializing gadget'
        twisted.web.widgets.Gadget.__init__(self)
        self.pageFactory = Page
        
    def getChild(self, path, request):
        m = MList(foo.list)
        v = VList(m, 'example.xhtml')
        c = CList(m)
        c.setView(v)
        return v
    
def updateApplication(app, config):
    port = config['port']
    root = Gadget()
    site = server.Site(root)
    app.listenTCP(port, site)

root = Gadget()
site = server.Site(root)

