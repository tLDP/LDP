import PloneCVSFile

from Products.CVSFile.CVSSandboxRegistry import manage_addCVSSandboxRegistryForm, \
     manage_addCVSSandboxRegistry, findCVSSandboxRegistry

from Products.ExternalFile.CreationDialog import manage_add_via_gui, \
     confirm_create_form, confirm_create_action, conflict_create_form, \
     create_standard_formpart, create_externalfile_formpart

from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore import utils

from socket import gethostname

factory_type_information = (
    {'id': 'CMF CVS File',
     'content_icon': 'www/fish.gif',
     'meta_type': 'CMFCVSFile',
     'product': 'PloneCVSFile',
     'factory': 'addPloneCVSFile',
     'immediate_view': 'index_html',
     'actions': ({'id': 'view',
                  'name': 'View',
                  'action': 'wikipage_view',
                  'permissions': ('View CVS File',)},
                 {'id': 'comment',
                  'name': 'Comment',
                  'action': 'wikipage_comment_form',
                  'permissions': ('Add CVS File Comment',)},
                 {'id': 'edit',
                  'name': 'Edit',
                  'action': 'wikipage_edit_form',
                  'permissions': ('Edit CVS File',)},
                 {'id': 'create',
                  'name': 'Create',
                  'category': 'folder',
                  'action':'wikipage_create_form',
                  'permissions': ('Create CVS File',),
                  'visible': 0 },
                 ),
     },
    )

def initialize(context):
    """Initialize the Lampadas product."""

    context.registerClass(
        PloneCVSFile.PloneCVSFile,
        constructors = (
            PloneCVSFile.manage_addForm,
            PloneCVSFile.cvsregistry_formpart,
            PloneCVSFile.cvssandbox_formpart,
            create_externalfile_formpart,
            create_standard_formpart,
            findCVSSandboxRegistry,
            manage_add_via_gui,
            confirm_create_form,
            confirm_create_action,
            gethostname,
            PloneCVSFile.manage_add,
            PloneCVSFile.manage_add_with_upload
        ),
        icon = 'www/fish.gif'
    )

    # CMF Initialization
    registerDirectory('skins', globals())
    utils.ContentInit(
        'CVS File Content',
        content_types = (PloneCVSFile.PloneCVSFile,),
        permission = 'Create CVS File',
        extra_constructors = (PloneCVSFile.manage_add,),
        fti = factory_type_information,
        ).initialize(context)


