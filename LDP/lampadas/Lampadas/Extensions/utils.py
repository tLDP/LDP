from Products.CMFCore.TypesTool import  FactoryTypeInformation
from Products.CMFCore.DirectoryView import addDirectoryViews, registerDirectory, createDirectoryView
from Products.CMFCore.utils import getToolByName
from Products.CMFTypes.debug import log, log_exc
from Products.CMFTypes.utils import findDict
from Products.Lampadas import types_globals
from Globals import package_home

import sys, traceback

PRODUCT_NAME = 'Lampadas'
SKIN_DIRS = ['lampadas_templates', 'lampadas_scripts']

def install_tool(self, out):
    if not hasattr(self, "content_tool"):
        addTool = self.manage_addProduct[PRODUCT_NAME].manage_addTool
        addTool(PRODUCT_NAME + ' Content Tool')

    #and the tool uses an index
    catalog = getToolByName(self, 'portal_catalog')
    try:
        catalog.addIndex('UID', 'FieldIndex', extra=None)
    except:
        pass

    try:
        if not 'UID' in catalog.schema():
            catalog.addColumn('UID')
    except:
        print >> out, ''.join(traceback.format_exception(*sys.exc_info()))
        print >> out, "Problem updating catalog for UIDs"

    #reindex the objects already in the system
    #this might be an 'update' and not an install
    ct = getToolByName(self, "content_tool")
    ct.index()
    try:
        catalog.manage_reindexIndex(ids=('UID',))
    except:
        pass
    

def install_subskin(self, out, skin_name, globals=types_globals):
    homedir=package_home(globals)
    log('Skins are in the %s subdirectory of %s' % (skin_name, homedir))
    skinstool=getToolByName(self, 'portal_skins')
    if skin_name not in skinstool.objectIds():
        registerDirectory(skin_name, homedir)
        try:
            addDirectoryViews(skinstool, skin_name, homedir)
        except:
            pass

    for skinName in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skinName) 
        path = [i.strip() for i in  path.split(',')]

        # Delete it if it already exists, so it only exists once.
        for skin_dir in SKIN_DIRS:
            if skin_dir in path:
                path.remove(skin_dir)

            try:
                if skin_dir not in path:
                    path.insert(path.index('custom') +1, skin_dir)
            except ValueError:
                if skin_dir not in path:
                    path.append(skin_dir)  

        path = ','.join(path)
        skinstool.addSkinSelection( skinName, path)


def install_types(self, out, types, package_name):
    typesTool = getToolByName(self, 'portal_types')
    for type in types:
        try:
            typesTool._delObject(type.__name__)
        except:
            pass
        typesTool.manage_addTypeInformation(FactoryTypeInformation.meta_type,
                                            id=type.__name__,
                                            typeinfo_name="%s: %s" %(package_name, type.__name__))
        # set the human readable title explicitly
        t = getattr(typesTool, type.__name__, None)
        if t:
            t.title = type.portal_type
        

def install_validation(self, out, types, metadatatype):
    form_tool = getToolByName(self, 'portal_form')
    for type in types:
        key = type.meta_type.lower()
        form_tool.setValidators("%s_edit_form" % key, ['validate_id', 'validate_%s_edit' % key])
        
    #And the metadata handler
    if metadatatype:
        form_tool.setValidators("%s_edit_form" % metadatatype.__name__.lower(), [])
    else:
        form_tool.setValidators("extensiblemetadata_edit_form", [])

    #And references
    form_tool.setValidators('reference_edit', [])

def install_navigation(self, out, types, metadatatype):
    nav_tool = getToolByName(self, 'portal_navigation')

    #Generic
    script = "content_edit" 
    nav_tool.addTransitionFor('default', script , 'failure', 'action:edit')
    nav_tool.addTransitionFor('default', script, 'success', 'action:view')

    #Metadata handling
    if metadatatype:
        mdname = metadatatype.__name__.lower()
    else:
        mdname = "extensiblemetadata"
        
    nav_tool.addTransitionFor('default', '%s_edit_form' % mdname, 'failure', '%s_edit_form' % mdname)
    nav_tool.addTransitionFor('default', '%s_edit_form' % mdname, 'success', 'script:content_edit')

    #Type Specific
    for type in types:
        key    = type.meta_type.lower()
        page   = "%s_edit_form" % key
        nav_tool.addTransitionFor('default', page, 'success', 'script:%s' % script)
        nav_tool.addTransitionFor('default', page, 'failure', page)

    #And References
    nav_tool.addTransitionFor('default', 'reference_edit', 'success', 'pasteReference')
    nav_tool.addTransitionFor('default', 'reference_edit', 'failure', 'url:reference_edit')

def install_actions(self, out, types, metadatatype=None):
    print >> out, 'Installing actions...'
    typesTool = getToolByName(self, 'portal_types')
    for type in types:
        typeInfo = getattr(typesTool, type.__name__)
        if hasattr(type,'actions'):
            #Look for each action we define in type.actions
            #in typeInfo.action replacing it if its there and
            #just adding it if not
            new = list(typeInfo._actions)
            for action in type.actions:
                hit = findDict(typeInfo._actions, 'id', action['id'])
                if hit:
                    hit.update(action)
                else:
                    new.append(action)
            typeInfo._actions = tuple(new)

        if hasattr(type,'factory_type_information'):
            print >> out, 'factory_type_information for ', type
            print >> out, type.factory_type_information
            typeInfo.__dict__.update(type.factory_type_information)
            typeInfo._p_changed = 1
        else:
            print >> out, 'type ', type, ' has no factory_type_information.'


def installTypes(self, out, types, package_name, metadatatype=None):
    """Use this for your site with your types"""
    print >> out, 'Installing types: %s', types, ' into ', package_name
    install_tool(self, out)
    install_subskin(self, out, 'skins')
    install_types(self, out, types, package_name)
    install_validation(self, out, types, metadatatype)
    install_navigation(self, out, types, metadatatype)
    install_actions(self, out, types, metadatatype)
    
