"""
I am an extension of CVSFile that adds CMF functionality.
"""

from AccessControl import ClassSecurityInfo
from Products.Lampadas import registerType
from Products.CMFTypes.BaseContent import BaseContent
from Products.CMFTypes.ExtensibleMetadata import ExtensibleMetadata
from Products.CMFTypes.Field       import *
from Products.CMFTypes.Form        import *
from Products.CMFTypes.debug import log

# Base classes, peer classes
from Products.ExternalFile.ExternalFile import ExternalFile
from Products.CVSFile.CVSSandboxRegistry import findCVSSandboxRegistry # CVSSandboxRegistry, 

from Products.CMFCore.PortalContent import PortalContent

# CVSFile imports
from Products.CVSFile.CVSFile import CVSFile
from Products.CVSFile.ICVSFile import ICVSFile

# Zope builtins
import Globals  # InitializeClass (security stuff)

# Python builtins
import os

cmfcvsfile_globals = globals()

def addLampadasCVSFile(self, id, **kwargs):
    o = LampadasCVSFile(id, **kwargs)
    self._setObject(id, o)

class LampadasCVSFile(BaseContent):
    """Extended from CVSFile
    """

    portal_type = 'Lampadas CVSFile'
    meta_type = 'LampadasCVSFile'

    type = BaseContent.type + FieldList((
#        Field('title',
#              searchable=1),
#        Field('description',
#              searchable=1),
#        Field('abstract',
#              searchable=1,
#              form_info=TextAreaInfo(description="A textual description of the content of the resource (e.g., an abstract, contents note).",
#                                     label="Abstract",
#                                     rows=3)),
        Field('body',
              required=0,
              searchable=1,
              allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword'),
              form_info=RichFormInfo(description="Enter a valid body for this document. This is what you will see",
                                     label="Body Text",
                                     )),
        Field('filepath',
              default='',
              accessor='getFilepath',
              mutator='setFilepath'),
#        Field('mime_type'),
        Field('behave_like',
              default='DTMLDocument',
              accessor='getBehaveLike',
              mutator='setBehaveLike',
              vocabulary=DisplayList((('DTMLDocument', 'DTMLDocument'),
                                      ('DTMLMethod',   'DTMLMethod'),
                                      ('File',         'File'),
                                      ('Image',        'Image'),
                                      ('PageTemplate', 'PageTemplate'))),
              form_info=SingleSelectionInfo(format='pulldown',
                                            label='Behave Like',
                                            description='Determines how the file is managed.'))
        ))

    manage_options = PortalContent.manage_options
    
registerType(LampadasCVSFile)

