"""
I am an extension of CVSFile that adds CMF functionality.
"""

# Base classes, peer classes
from Products.ExternalFile.ExternalFile import ExternalFile
from Products.CVSFile.CVSSandboxRegistry import findCVSSandboxRegistry # CVSSandboxRegistry, 

# Zope builtins
from Globals import DTMLFile #, MessageDialog
from AccessControl import ClassSecurityInfo
import Globals  # InitializeClass (security stuff)

# CVSFile imports
from Products.CVSFile.CVSFile import CVSFile
from Products.CVSFile.ICVSFile import ICVSFile

# CMFCore imports
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.PortalContent import PortalContent
from Products.CMFCore.CMFCatalogAware import CMFCatalogAware
from Products.CMFCore.DynamicType import DynamicType
from Products.CMFDefault.File import File

# OFS imports
from OFS.SimpleItem import SimpleItem
from OFS import Image

# OMF imports
from OMF import OMF

# Local imports
from Defaults import META_TYPE, PORTAL_TYPE

# Python builtins
import os
from DateTime import DateTime

################################################################
# Container Methods
################################################################

# globals() is standard python for passing the current namespace
manage_addForm       = Globals.DTMLFile('dtml/create',               globals())
cvsregistry_formpart = DTMLFile('dtml/cvsregistry_formpart', globals())
cvssandbox_formpart  = DTMLFile('dtml/cvssandbox_formpart',  globals())

cmfcvsfile_globals = globals()

default_perms = {
    'create':   'nonanon',
    'edit':     'nonanon',
    'comment':  'nonanon',
    'move':     'nonanon'}

def initMetadata(object):
    object.creation_date = DateTime()
    object._editMetadata(title='',
                         subject=(),
                         description='',
                         contributors=(),
                         effective_date=None,
                         expiration_date=None,
                         format='text/plain',
                         language='',
                         rights='',
                         authors = (),
                         maintainers = (),
                         versions = (),
                         types = (),
                         formats = (),
                         identifiers = (),
                         sources = (),
                         relations = (),
                         coverages = ()
                         )

def makeCMFCVSFile(id, title, description, target_filepath):
    object = PloneCVSFile(id,
                          title           = title,
                          description     = description,
                          target_filepath = target_filepath)
    object.title = title
    object.parents = []
    username = getSecurityManager().getUser().getUserName()
    obj.manage_addLocalRoles(username, ['Owner'])
    object._getRegs().setSubOwner('both')
    initMetadata(object)

def manage_add(self,
               id, title='', description='', 
               target_filepath='', basedir='', REQUEST=None):
    """Factory method to actually create an instance of CMFCVSFile.
    """

    id = str(id)
    title = str(id)
    object = makeCMFCVSFile(id, title, description, target_filepath)
    self._setObject(id, object)
    self._getOb(id).reindex_object()

def manage_add_with_upload(self,
                           id, title, description,
                           target_filepath, upload_file, basedir,
                           REQUEST=None):
    """Factory method to actually create an instance of PloneCVSFile.
    """
    fully_resolved_target_filepath = os.path.join(basedir,target_filepath)    

    copy_file(upload_file, fully_resolved_target_filepath)
    
    self._setObject(id, PloneCVSFile(id, title, description,
                                target_filepath))
    self._getOb(id).reindex_object()


################################################################
# CVSFile class
################################################################

# PortalContent brings in: DynamicType, CMFCatalogAware, SimpleItem

class PloneCVSFile(CVSFile, File, PortalContent, OMF):

    """Extended from CVSFile
    """

    __implements__ = (CVSFile.__implements__,
                      PortalContent.__implements__,
                      OMF.__implements__)
    
    isPortalContent = 1
    _isPortalContent = 1
    
    _isTypeInformation = 1
    
    meta_type = META_TYPE
    portal_type = PORTAL_TYPE

    _isDiscussable = 1


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
    
    def __init__(self, id, title='', description='', relativeFilePath='', ):
        CVSFile.__init__(self, id, title, description, relativeFilePath)
        File.__init__(self, id, title, relativeFilePath)
        OMF.__init__(self)
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
    def setTitle(self, ttle):
        """Set ths ttle property."""
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
        
# register security information
Globals.InitializeClass(PloneCVSFile)
