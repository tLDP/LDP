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

# CVSFile imports
from Products.CVSFile.CVSFile import CVSFile
from Products.CVSFile.ICVSFile import ICVSFile

# Zope builtins
from Globals import DTMLFile #, MessageDialog
import Globals  # InitializeClass (security stuff)

# CMFCore imports
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.PortalContent import PortalContent
from Products.CMFCore.CMFCatalogAware import CMFCatalogAware
from Products.CMFCore.DynamicType import DynamicType
from Products.CMFDefault.File import File

# Python builtins
import os
from DateTime import DateTime

################################################################
# Container Methods
################################################################

# globals() is standard python for passing the current namespace
manage_addForm       = DTMLFile('dtml/create',               globals())
cvsregistry_formpart = DTMLFile('dtml/cvsregistry_formpart', globals())
cvssandbox_formpart  = DTMLFile('dtml/cvssandbox_formpart',  globals())

cmfcvsfile_globals = globals()

def addLampadasCVSFile(self, id, **kwargs):
    o = LampadasCVSFile(id, **kwargs)
    self._setObject(id, o)

class LampadasCVSFile(CVSFile, BaseContent):
    """Extended from CVSFile
    """

    portal_type = 'Lampadas CVSFile'
    meta_type = 'LampadasCVSFile'

    type = BaseContent.type

    # This tuple defines a dictionary for each tab in the management interface
    # label = label of tab, action = url it links to
    manage_options = ( ExternalFile.manage_options + (
    	{'label':'CVS',	          'action': 'manage_cvsForm'},
        {'label':'OMF Meta-data', 'action': 'manage_metadata'}
    ) +  CMFCatalogAware.manage_options )

    security = ClassSecurityInfo()

    # set security for the object itself, e.g. if it is accessed in DTML code
    # This line is REQUIRED to allow access to CVSFiles by the public (ariel DTDs, etc.)
    security.declareObjectPublic()

    # call __call__() method on DTMLFile for our edit form, point at our cvs_form.dtml
    # globals() is standard python for passing the current namespace
    cvs_form           = DTMLFile('dtml/cvs_form',globals())
    
    security.declareProtected('Manage CVS Files',      'manage_cvsForm')
    manage_cvsForm     = DTMLFile('dtml/cvs',globals())
    
    # these lines exist so we can call them from DTML
    cvsregistry_formpart = cvsregistry_formpart
    cvssandbox_formpart  = cvssandbox_formpart
    # end of DTML scoping hack

    # CMF ATTRIBUTES

    set = security.setPermissionDefault
    set('Edit CVS File', ('Owner', 'Manager', 'Authenticated'))
    set('FTP Access', ('Owner', 'Manager', 'Authenticated'))
    set('Create CVS File', ('Owner', 'Manager'))
    set('Move CVS File', ('Owner', 'Manager'))
    set('Add CVSFile comment', ('Owner', 'Manager', 'Authenticated'))
    set = None

    manage_metadata = DTMLFile('dtml/omf_metadata', globals())
    
    def __init__(self, id='foo', title='', description='', relativeFilePath='', ):
        CVSFile.__init__(self, id, title, description, relativeFilePath)
        BaseContent.__init__(self, id)
        self.data = ''
    
    def inCMF(self):
        """Return true if this object is in a CMF portal.
        """
        return hasattr(self.aq_inner.aq_parent,'portal_membership')
    
    security.declarePublic('getId')
    def getId(self):
        try: return self.id()
        except TypeError: return self.id
    
    security.declareProtected(CMFCorePermissions.View, 'SearchableText')
    def SearchableText(self):
        return self.getContents()

    security.declarePublic('getContents')
    def getContents(self, REQUEST=None, RESPONSE=None):
        """Returns the contents of the file if possible."""
        return CVSFile.getContents(self, REQUEST, RESPONSE)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setFileInfo')
    def setFileInfo(self, filepath='', title='', description=''):
        """Sets meta-data from the CVS properties screen.
        """
        self.setTitle(title)
        self.setDescription(description)
        self.setFilepath(filepath)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setTitle')
    def setTitle(self, title):
        """Set ths title property."""
        self.title = title
        
    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setDescription')
    def setDescription(self, description):
        """Set ths description property."""
        self.description = description
        
    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setFilepath')
    def setFilepath(self, filepath):
        """Set ths filepath property."""
        self.filepath = filepath
        self.data = self.getContents()
        
registerType(LampadasCVSFile)

