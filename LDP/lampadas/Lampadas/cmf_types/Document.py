from AccessControl import ClassSecurityInfo, Permissions
from Products.Lampadas import registerType
from Products.CMFTypes.BaseFolder import BaseFolder
from Products.CMFTypes.ExtensibleMetadata import ExtensibleMetadata
from Products.CMFTypes.Field       import *
from Products.CMFTypes.Form        import *
from Products.CMFTypes.debug import log

from Products.CMFDefault.SkinnedFolder import SkinnedFolder

from Products.CMFCore import CMFCorePermissions

from Products.CMFCore.PortalContent import PortalContent

from utils import unique_options


def addLampadasDocument(self, id, **kwargs):
    o = LampadasDocument(id, **kwargs)
    self._setObject(id, o)

class LampadasDocument(BaseFolder):
    """A Lampadas-enabled CMF Document type."""

    portal_type = "Lampadas Document"
    meta_type = "LampadasDocument"

    type       = BaseFolder.type + FieldList((
        Field('abstract',
              searchable=1,
              form_info=TextAreaInfo(description="A textual description of the content of the resource (e.g., an abstract, contents note).",
                                     label="Abstract",
                                     rows=3)),
        Field('author'),
        Field('body',
              required=0,
              searchable=1,
              allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword'),
              form_info=RichFormInfo(description="Enter a valid body for this document. This is what you will see",
                                     label="Body Text",
                                     )),

#        IntegerField("number", form_info=IntegerInfo(), default=42),

#        Field('image', form_info=FileInfo()),
        
#        SlotField("about",
#                  form_info=SlotInfo(slot_metal="here/about_slot/macros/aboutBox",
#                                     )),
        ))
    
    # These are *additional* actions, in addition to those already provided
    # by the base type.
    actions = ( { 'id'            : 'foldercontents'
                , 'name'          : 'Contents'
                , 'action'        : 'folder_contents'
                , 'permissions'   :
                   (Permissions.access_contents_information,)
                , 'category'      : 'object'
                }
              , { 'id'            : 'local_roles'
                , 'name'          : 'Local Roles'
                , 'action'        : 'folder_localrole_form'
                , 'permissions'   :
                   (CMFCorePermissions.ManageProperties,)
                , 'category'      : 'object'
                }
              , { 'id'            : 'render_html'
                , 'name'          : 'Render HTML'
                , 'action'        : 'render_html'
                , 'permissions'   :
                   (CMFCorePermissions.ManageProperties,)
                , 'category'      : 'object'
                }
              )

    factory_type_information = { 'id': 'LampadasDocument',
                                 'description'    : """\
    Lampadas documents can hold source files and generate output files."""
                               , 'content_icon'   : 'folder_icon.gif'
                               , 'filter_content_types' : 0
                               , 'immediate_view' : 'portal_form/folder_contents'}

    manage_options = unique_options(SkinnedFolder.manage_options + \
                                    PortalContent.manage_options,)

registerType(LampadasDocument)

