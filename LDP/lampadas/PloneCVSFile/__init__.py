import PloneCVSFile

from Products.CVSFile.CVSSandboxRegistry import manage_addCVSSandboxRegistryForm, \
     manage_addCVSSandboxRegistry, findCVSSandboxRegistry

from Products.ExternalFile.CreationDialog import manage_add_via_gui, \
     confirm_create_form, confirm_create_action, conflict_create_form, \
     create_standard_formpart, create_externalfile_formpart

from socket import gethostname

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

