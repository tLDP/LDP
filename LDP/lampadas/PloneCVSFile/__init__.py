import PloneCVSFile

from Products.CVSFile.CVSSandboxRegistry import manage_addCVSSandboxRegistryForm, \
     manage_addCVSSandboxRegistry, findCVSSandboxRegistry

from Products.ExternalFile.CreationDialog import manage_add_via_gui, \
     confirm_create_form, confirm_create_action, conflict_create_form, \
     create_standard_formpart, create_externalfile_formpart

from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore import utils, CMFCorePermissions

from Products.CMFDefault import Portal

from OMF import OMF
from Defaults import META_TYPE

from socket import gethostname

factory_type_information = (
    {'id': 'CMF CVS File',
     'meta_type': META_TYPE,
     'description': 'A file in a CVS repository.',
     'content_icon': 'file_icon.gif',
     'icon': 'file_icon.gif',
     'product': 'PloneCVSFile',
     'factory': 'addPloneCVSFile',
     'immediate_view': 'metadata_edit_form',
     'actions': ({'id': 'view',
                  'name': 'View',
                  'action': 'view',
                  'permissions': (CMFCorePermissions.View,)},
                 {'id': 'file view',
                  'name': 'View',
                  'action': 'file_view',
                  'permissions': (CMFCorePermissions.View,)},
                 {'id': 'edit',
                  'name': 'Edit',
                  'action': 'file_edit_form',
                  'permissions': (CMFCorePermissions.ModifyPortalContent,)},
                 {'id': 'metadata',
                  'name': 'Metadata',
                  'action': 'metadata_edit_form',
                  'permissions': (CMFCorePermissions.ModifyPortalContent,)},
                 )
     },
    )

bases = (Portal.CMFSite,
          OMF,
          PloneCVSFile.PloneCVSFile)

import sys
this_module = sys.modules[__name__]

z_bases = utils.initializeBasesPhase1(bases, this_module)

plonecvsfile_globals = globals()
registerDirectory('skins', globals())

def initialize(context):
    """Initialize the Lampadas product."""

#    context.registerClass(
#        PloneCVSFile.PloneCVSFile,
#        constructors = (
#            PloneCVSFile.manage_addForm,
#            PloneCVSFile.cvsregistry_formpart,
#            PloneCVSFile.cvssandbox_formpart,
#            create_externalfile_formpart,
#            create_standard_formpart,
#            findCVSSandboxRegistry,
#            manage_add_via_gui,
#            confirm_create_form,
#            confirm_create_action,
#            gethostname,
#            PloneCVSFile.manage_add,
#            PloneCVSFile.manage_add_with_upload
#        ),
#        icon = 'www/fish.gif'
#    )

    # CMF Initialization
    utils.initializeBasesPhase2(z_bases, context)
    utils.ContentInit(
        meta_type = 'CVS File Content',
        content_types = (PloneCVSFile.PloneCVSFile,),
        permission = 'Create CVS File',
        extra_constructors = (PloneCVSFile.manage_add,),
        fti = factory_type_information,
        ).initialize(context)
    context.registerClass(PloneCVSFile.PloneCVSFile,
        constructors=(PloneCVSFile.manage_addForm,
                      PloneCVSFile.manage_add,),
        )
                      
