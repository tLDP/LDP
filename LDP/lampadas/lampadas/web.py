#!/usr/bin/python

from twisted.internet import app
from twisted.web import server, widgets
from twisted.python import usage
from twisted.web.resource import Resource
from twisted.internet import reactor
from objects import object_server

class Options(usage.Options):
    optParameters = [["port", "p", 8080,
                      "Port to listen with Webserver"]]
    
class Page(widgets.WidgetPage):
    template = '<html><head></head><body>%%%%self.widget%%%%</body></html>'

class Gadget(widgets.Gadget):
    def __init__(self):
        print 'Initializing gadget'
        widgets.Gadget.__init__(self)
        self.pageFactory = Page
        self.putWidget('hello', HelloWorld())
        self.putWidget('', HelloWorld())
        print 'connecting object_server...'
        object_server.connect(self.connected)

    def connected(self, message):
        print 'object server is connected, loading pages...'
        object_server.page.get_all(self.loaded)

    def loaded(self, pages):
        print 'Pages loaded:'
        for row in pages:
            page = WebPage()
            page.row = row
            self.putWidget(page.row.page_code, page)
        
class WebPage(widgets.Widget):
    def display(self, request):
        return [self.row.page_code]

class HelloWorld(widgets.Widget):
    def display(self, request):
        return ['Hello, world!']
        
def updateApplication(app, config):
    port = config['port']
    root = Gadget()
    site = server.Site(root)
    app.listenTCP(port, site)

root = Gadget()
site = server.Site(root)
