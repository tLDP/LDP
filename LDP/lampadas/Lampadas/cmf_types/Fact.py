from AccessControl import ClassSecurityInfo
#from Products.CMFTypes import registerType
from Products.Lampadas import registerType
from Products.CMFTypes.BaseContent import BaseContent
from Products.CMFTypes.ExtensibleMetadata import ExtensibleMetadata
from Products.CMFTypes.Field       import *
from Products.CMFTypes.Form        import *
from Products.CMFTypes.debug import log


def addFact(self, id, **kwargs):
    o = Fact(id, **kwargs)
    self._setObject(id, o)

class Fact(BaseContent):
    """A quoteable fact or tidbit"""
    portal_type = meta_type = "Fact"
    
    type = BaseContent.type + FieldList((
        Field('quote',
              searchable=1,
              required=1,
              form_info=StringInfo(description="What are you quoting, what is the fact",
                                   label="Quote",
                                   )),

        LinesField('sources', form_info=LinesInfo()),
        
        Field('footnote',
              required=1,
              form_info = TextAreaInfo(description="The full footnot for this fact/quote")),
        
        DateTimeField('fact_date',
                      form_info=DateTimeInfo(description="When does this fact originate from",
                                             label="Date")),
        
        Field('url',
              form_info=LinkInfo(description="When does this fact originate from",
                                 label="URL")),
        
        ))
    
registerType(Fact)

