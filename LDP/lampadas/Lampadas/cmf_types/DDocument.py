from AccessControl import ClassSecurityInfo
#from Products.CMFTypes import registerType
from Products.Lampadas import registerType
from Products.CMFTypes.BaseContent import BaseContent
from Products.CMFTypes.ExtensibleMetadata import ExtensibleMetadata
from Products.CMFTypes.Field       import *
from Products.CMFTypes.Form        import *
from Products.CMFTypes.debug import log


def addDDocument(self, id, **kwargs):
    o = DDocument(id, **kwargs)
    self._setObject(id, o)

class DDocument(BaseContent):
    """An extensible Document (test) type"""

    portal_type = meta_type = "DDocument"
    
    type       = BaseContent.type + FieldList((
        Field('teaser',
              searchable=1,
              form_info=TextAreaInfo(description="A short lead-in to the article so that we might get people to read the body",
                                     label="Teaser",
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
    
                  
registerType(DDocument)

