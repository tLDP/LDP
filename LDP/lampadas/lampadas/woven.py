#!/usr/bin/python

from twisted.internet import app
from twisted.web import server
from twisted.python import usage, components
from twisted.web.resource import Resource
from twisted.internet import reactor
from objects import object_server

from twisted.web.woven import model, view, controller, interfaces
from twisted.web.woven import widgets
from twisted.web import domhelpers
import cgi
import twisted.web

from Globals import state, VERSION
from URLParse import URI
from BaseClasses import LampadasCollection

# Custom Widgets
class I18nTextWidget(widgets.Text):
    def __init__(self, text, raw=1, lang='EN'):
        widgets.Text.__init__(self, text, raw=raw)
        self.lang = lang

    def getData(self):
        return widgets.Text.getData(self)[self.lang]

class I18nListWidget(widgets.List):
    def __init__(self, model=None, submodel=None, setup=None, lang='EN'):
        widgets.List.__init__(self, model, submodel, setup)
        self.lang = lang

    def getData(self):
        return widgets.List.getData(self)[self.lang]

class SectionBarWidget(widgets.Widget):
    def generateDOM(self, request, node):
        document = widgets.document

        self.cleanNode(node)

        tr_node = document.createElement('tr')
        node.appendChild(tr_node)

        for key in sections.sort_by('sort_order'):
            td_node = document.createElement('td')
            tr_node.appendChild(td_node)
            a_node = document.createElement('a')
            td_node.appendChild(a_node)
            
            section = sections[key].object
            href = '%ssection/%s%s' % (state.uri.base, section.section_code, state.uri.lang_ext)
            name = section.section_name[state.uri.lang]
            
            a_node.setAttribute('href', href)
            text_node = document.createTextNode(name)
            a_node.appendChild(text_node)
        return self.node

# Holds an MVC triad as well as the original row object in a neat package.
class MVC:
    def __init__(self, rowobject, business_object, object_model, object_view, object_controller):
        self.row = rowobject
        self.object = business_object
        self.model = object_model
        self.view = object_view
        self.controller = object_controller
        self.__dict__.update(rowobject.__dict__)
        self.object.__dict__.update(rowobject.__dict__)

# Parse strings, replacing tokens and text with appropriate widgets.
def replace_token(token):
    if token=='uri.base':
        return state.uri.base
    elif token=='uri.lang_ext':
        return state.uri.lang_ext
    elif token=='version':
        return VERSION
    elif token=='':
        return ''

    print 'Cannot replace token: ', token
    return '<font color="red">%s</font>' % token
    
def build_items(object, text):
    object.items = []
    counter = 0
    temp = text.replace('\|', 'DCM_PIPE')
    for piece in temp.split('|'):
        counter += 1
        is_text = counter % 2
        if is_text:
            piece = piece.replace('DCM_PIPE', '\|')
            if piece > '':
                object.items.append(piece)
        else:
            if strings.has_key(piece):
                object.items.append(strings[piece].string[lang])
            elif blocks.has_key(piece):
                object.items.append(blocks[piece].block[lang])
            else:
                newstring = replace_token(piece)
                object.items.append(newstring)
    return object.items

def build_lang_items(object, text):
    object.items = LampadasCollection()
    for lang in text.keys():
        counter = 0
        items = []
        temp = text[lang].replace('\|', 'DCM_PIPE')
        for piece in temp.split('|'):
            counter += 1
            is_text = counter % 2
            if is_text:
                piece = piece.replace('DCM_PIPE', '\|')
                if piece > '':
                    items.append(piece)
            else:
                if strings.has_key(piece):
                    items.append(strings[piece].string[lang])
                elif blocks.has_key(piece):
                    items.append(blocks[piece].block[lang])
                else:
                    newstring = replace_token(piece)
                    items.append(newstring)
        object.items[lang] = items
    return object.items

# Collections of MVC triads.
# Each collection has its own MVC, and each object in the collection does as well.
class Blocks(LampadasCollection, model.WModel):
    pass

class Block:
    pass

class Pages(LampadasCollection, model.WModel):
    pass

class Page:
    pass

class Sections(LampadasCollection, model.WModel):
    pass

class Section:
    pass

class Strings(LampadasCollection, model.WModel):
    pass

class String:
    pass

blocks = Blocks()
pages = Pages()
sections = Sections()
strings = Strings()

class MBlock(model.WModel):
    def __init__(self, rowobject):
        model.WModel.__init__(self)
        self.rowobject = rowobject
        self.block_code = rowobject.block_code
        self.block = rowobject.block
    
class VBlock(view.WView):
    def wvfactory_block_code(self, request, node, model):
        domhelpers.clearNode(node)
        return widgets.Text(model)
    
    def wvfactory_block(self, request, node, model):
        domhelpers.clearNode(node)
        return widgets.Text(model)
    
    def wvfactory_block_items(self, request, node, model):
        block_object = blocks[self.model.block_code].object
        build_items(block_object, block_object.block)
        return widgets.List(block_object.items)

class CBlock(controller.WController):
    pass

view.registerViewForModel(VBlock, MBlock)
controller.registerControllerForModel(CBlock, MBlock)
    

class MPage(model.WModel):
    def __init__(self, rowobject):
        model.WModel.__init__(self)
        self.__dict__.update(rowobject.__dict__)
    
class VPage(widgets.Widget):
    
    templateFile = 'index.xhtml'
    
    def setUp(self, request, document):
        pass

    def wvfactory_title(self, request, node, model):
        page_object = pages[self.model.page_code]
        build_lang_items(page_object.title, page_object.title)
        return widgets.List(page_object.title.items[self.lang])

        return I18nTextWidget(model, lang=self.lang)
    
    def wvfactory_page_code(self, request, node, model):
        return widgets.Text(model)
    
    def wvfactory_page(self, request, node, model):
        return I18nTextWidget(model, lang=self.lang)

    def wvfactory_page_items(self, request, node, model):
        page_object = pages[self.model.page_code].object
        build_lang_items(page_object, page_object.page)
        return widgets.List(page_object.items[self.lang])

    def wvfactory_menu(self, request, node, model):
        return widgets.List(sections.keys())

    def wvfactory_section_bar(self, request, node, model):
        return SectionBarWidget()

class CPage(controller.WController):
    pass

view.registerViewForModel(VPage, MPage)
controller.registerControllerForModel(CPage, MPage)


class MString(model.WModel):
    def __init__(self, rowobject):
        model.WModel.__init__(self)
        self.__dict__.update(rowobject.__dict__)
    
class VString(widgets.Widget):
    
    templateFile = 'index.xhtml'
    
    def setUp(self, request, document):
        pass

    def wvfactory_string_code(self, request, node, model):
        return widgets.Text(model)
    
    def wvfactory_string(self, request, node, model):
        return I18nTextWidget(model, lang=self.lang)
    
    def wvfactory_string_items(self, request, node, model):
        string_object = strings[self.model.string_code].object
        build_lang_items(string_object, string_object.string)
        return widgets.List(string_object.items[self.lang])

    def wvfactory_version(self, request, node, model):
        return I18nTextWidget(model, lang=self.lang)

class CString(controller.WController):
    pass

view.registerViewForModel(VString, MString)
controller.registerControllerForModel(CString, MString)


class MSection(model.DictionaryModel):
    def __init__(self, orig, *args, **kwargs):
        model.Model.__init__(self, *args, **kwargs)
        model.DictionaryModel.__init__(self, orig)

class VSection(widgets.Widget):
    def wvfactory_title(self, request, node, model):
        return widgets.List(model)
    
class CSection(controller.WController):
    pass

view.registerViewForModel(VSection, MSection)
controller.registerControllerForModel(CSection, MSection)


class MList(model.ListModel):
    def __init__(self, orig, *args, **kwargs):
        model.Model.__init__(self, *args, **kwargs)
        model.ListModel.__init__(self, orig)

class VList(widgets.Widget):
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
    
class WidgetPage(twisted.web.widgets.WidgetPage):
    template = '<html><head></head><body>%%%%self.widget%%%%</body></html>'

class Gadget(twisted.web.widgets.Gadget):
    def __init__(self):
        twisted.web.widgets.Gadget.__init__(self)
        self.tables_loaded = 0
        self.pageFactory = WidgetPage
        object_server.connect(self.connected)

    def connected(self, message):
        object_server.section.get_all(self.loaded_sections)
        object_server.string.get_all(self.loaded_strings)
        object_server.block.get_all(self.loaded_blocks)

    def loaded_blocks(self, blockrows):
        for blockrow in blockrows:
            block_object = Block()
            block_model = MBlock(blockrow)
            block_view = VBlock(block_model)
            block_controller = CBlock(block_model)
            block_controller.setView(block_view)
            block_mvc = MVC(blockrow, block_object, block_model, block_view, block_controller)
            blocks[blockrow.block_code] = block_mvc
        print 'Blocks loaded.'
        self.tables_loaded += 1
        if self.tables_loaded==3:
            self.load_pages()
       
    def load_pages(self):
        object_server.page.get_all(self.loaded_pages)

    def loaded_pages(self, pagerows):
        for pagerow in pagerows:
            page_object = Page()
            page_model = MPage(pagerow)
            page_view = VPage(page_model)
            page_controller = CPage(page_model)
            page_controller.setView(page_view)
            page_mvc = MVC(pagerow, page_object, page_model, page_view, page_controller)
            pages[pagerow.page_code] = page_mvc
        print 'Pages loaded.'
        
    def loaded_sections(self, sectionrows):
        for sectionrow in sectionrows:
            section_object = Section()
            section_model = MSection(sectionrow)
            section_view = VSection(section_model)
            section_controller = CSection(section_model)
            section_controller.setView(section_view)
            section_mvc = MVC(sectionrow, section_object, section_model, section_view, section_controller)
            sections[sectionrow.section_code] = section_mvc
        print 'Sections loaded.'
        self.tables_loaded += 1
        if self.tables_loaded==3:
            self.load_pages()
        
    def loaded_strings(self, stringrows):
        for stringrow in stringrows:
            string_object = String()
            string_model = MString(stringrow)
            string_view = VString(string_model)
            string_controller = CString(string_model)
            string_controller.setView(string_view)
            string_mvc = MVC(stringrow, string_object, string_model, string_view, string_controller)
            strings[stringrow.string_code] = string_mvc
        print 'Strings loaded.'
        self.tables_loaded += 1
        if self.tables_loaded==3:
            self.load_pages()
       
    def getChild(self, path, request):
        state.uri = URI(request.path)
        if pages.has_key(state.uri.page_code):
            resource = pages[state.uri.page_code].view
        else:
            resource = pages['404'].view
        resource.lang = state.uri.lang
        return resource
    
def updateApplication(app, config):
    port = config['port']
    root = Gadget()
    site = server.Site(root)
    app.listenTCP(port, site)

root = Gadget()
site = server.Site(root)

