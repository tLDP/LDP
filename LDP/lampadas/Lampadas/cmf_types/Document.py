from AccessControl import ClassSecurityInfo
from Products.Lampadas import registerType
from Products.CMFTypes.BaseContent import BaseContent
from Products.CMFTypes.ExtensibleMetadata import ExtensibleMetadata
from Products.CMFTypes.Field       import *
from Products.CMFTypes.Form        import *
from Products.CMFTypes.debug import log


def addLampadasDocument(self, id, **kwargs):
    o = LampadasDocument(id, **kwargs)
    self._setObject(id, o)

class LampadasDocument(BaseContent):
    """A Lampadas-enabled CMF Document type."""

    portal_type = "Lampadas Document"
    meta_type = "LampadasDocument"
    
    type       = BaseContent.type + FieldList((
        Field('abstract',
              searchable=1,
              form_info=TextAreaInfo(description="A textual description of the content of the resource (e.g., an abstract, contents note).",
                                     label="Abstract",
                                     rows=3)),
        Field('author'),
        Field('body',
              required=1,
              searchable=1,
              allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword'),
              form_info=RichFormInfo(description="Enter a valid body for this document. This is what you will see",
                                     label="Body Text",
                                     )),

        IntegerField("number", form_info=IntegerInfo(), default=42),

        Field('image', form_info=FileInfo()),
        
#        SlotField("about",
#                  form_info=SlotInfo(slot_metal="here/about_slot/macros/aboutBox",
#                                     )),
        ))
    
                  
registerType(LampadasDocument)

