from Products.CMFTypes import process_types
from Products.CMFTypes.Generator import generateViews
from Products.CMFTypes.utils import pathFor
from Products.CMFTypes.ExtensibleMetadata import ExtensibleMetadata
from Globals import package_home

from Products.CMFCore.utils import ContentInit
import os, os.path

ADD_CONTENT_PERMISSION = 'Add portal content'
PROJECT_NAME = 'Lampadas'

types_globals = globals()

_types = {}

def registerType(type):
    print 'Registering %s meta_type in Lampadas' % type.meta_type
    _types[type.meta_type] = type
    
def listTypes():
    return _types.values()

def initialize(context):
    import cmf_types        

    print 'Initializing Lampadas product.'
    print 'dir() is ', dir()
    print 'dir(cmf_types) is ', dir(cmf_types)
    
    homedir = package_home(globals())
    edit_dir = view_dir = os.path.join(homedir, 'skins', 'lampadas_templates')
    script_dir = os.path.join(homedir, 'skins', 'lampadas_scripts')
    
    content_types, constructors, ftis = process_types(listTypes(),
                                                      "Lampadas",
                                                      edit_dir=edit_dir,
                                                      view_dir=view_dir,
                                                      script_dir=script_dir)
    ContentInit(
        PROJECT_NAME + ' Content',
        content_types = content_types,
        permission = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti = ftis,
        ).initialize(context)

