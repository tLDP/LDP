#!/usr/bin/python

from twisted.web.woven import model, view, controller
from twisted.web.woven import widgets, input
from twisted.web import domhelpers

#from TwistedQuotes import quoters


import cgi

class MQuote(model.WModel):
    def __init__(self):
        print 'Loading MQuote'
        model.WModel.__init__(self)
        #self._filename = filename
        #self._quoter = quoters.FortuneQuoter([filename])
        self.quote = "Hello, world!"
        self.title = "Quotes Galore!"
        self.newQuote = ""

    def updateQuote(self):
        self.quote = 'Hello, world!'

class QuoteWidget(widgets.Widget):
    def setUp(self, request, node, data):
        """
        Set up this Widget object before it gets rendered into HTML.

        Since self is a Widget, I can use the higher level widget API to add a 
        Text widget to self. I then rely on Widget.generateDOM to convert
        from Widgets into the Document Object Model.
        """
        self.add(widgets.Text(cgi.escape(data)))


class VQuote(view.WView):
    templateFile = "home.xhtml"

    def setUp(self, request, document):
        """
        Set things up for this request.
        """
        self.model.updateQuote()

    def wvfactory_quote(self, request, node, model):
        """Create a widget which knows how to render my model's quote."""
        domhelpers.clearNode(node)
        return QuoteWidget(model)

    def wvfactory_title(self, request, node, model):
        """Create a widget which knows how to render my model's title."""
        domhelpers.clearNode(node)
        return widgets.Text(model)


class NewQuoteHandler(input.SingleValue):
    def check(self, request, data):
        if data:
            return 1

    def commit(self, request, node, newQuote):
        print "committing new quote", `newQuote`
        file = open(self.model.getQuoteFilename(), 'a')
        file.write('\n%\n'  + newQuote)


class CQuote(controller.WController):
    def wcfactory_newQuote(self, model):
        """Create a handler which knows how to verify input in a form with the
        name "newQuote"."""
        return NewQuoteHandler(model)


view.registerViewForModel(VQuote, MQuote)
controller.registerControllerForModel(CQuote, MQuote)

