"""
I am an extension of CVSFile that adds CMF functionality.
"""

# Base classes, peer classes
from Products.ExternalFile.ExternalFile import ExternalFile
from Products.CVSFile.CVSSandboxRegistry import findCVSSandboxRegistry # CVSSandboxRegistry, 
#from SandboxInfo import SandboxInfo
#from OSUtils import runCommand, command_separator
#from Products.ExternalFile.FileUtils import copy_file

# Zope builtins
from Globals import DTMLFile #, MessageDialog
from AccessControl import ClassSecurityInfo
import Globals  # InitializeClass (security stuff)

# CVSFile imports
from Products.CVSFile.CVSFile import CVSFile
from Products.CVSFile.ICVSFile import ICVSFile

# CMFCore imports
from Products.CMFCore.PortalContent import PortalContent

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
                         rights='')

def makeCMFCVSFile(id, title, description, target_filepath):
    object = PloneCVSFile(id, title, description, target_filepath)
    object.title = title
    object.parents = []
    username = getSecurityManager().getUser().getUserName()
    obj.manage_addLocalRoles(username, ['Owner'])
    object._getRegs().setSubOwner('both')
    initMetadata(object)

def manage_add(self,
               id, title='', description='', 
               target_filepath='README', basedir='', REQUEST=None):
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

def manage_lampadas(self, action, REQUEST=None):
    """Perform a Lampadas action on the file, i.e., convert it.
    """
    pass


################################################################
# CVSFile class
################################################################

class PloneCVSFile(CVSFile, PortalContent):

    """Extended from CVSFile
    """

    def __init__(self, id, title='', description='', relativeFilePath='foo.html'):
        CVSFile.__init__(self, id, title, description, relativeFilePath)
        
    
    meta_type = 'CMFCVSFile'  # This is the name Zope will use for the Product in
                              # the "addProduct" list

    __implements__ = ICVSFile

    # This tuple defines a dictionary for each tab in the management interface
    # label = label of tab, action = url it links to
    manage_options = ExternalFile.manage_options + (
	{'label':'CVS',	     'action': 'manage_cvsForm'},
    {'label':'Lampadas', 'action': 'manage_lampadasForm'}
        )

    _security = ClassSecurityInfo()

    # set security for the object itself, e.g. if it is accessed in DTML code
    # This line is REQUIRED to allow access to CVSFiles by the public (ariel DTDs, etc.)
    _security.declareObjectPublic()

    # call __call__() method on DTMLFile for our edit form, point at our cvs_form.dtml
    # globals() is standard python for passing the current namespace
    cvs_form           = DTMLFile('dtml/cvs_form',globals())
    
    _security.declareProtected('Manage CVS Files',      'manage_cvsForm')
    manage_cvsForm     = DTMLFile('dtml/cvs',globals())
    
    # these lines exist so we can call them from DTML
    cvsregistry_formpart = cvsregistry_formpart
    cvssandbox_formpart  = cvssandbox_formpart
    # end of DTML scoping hack

    # Lampadas extensions start here
    lampadas_cvs_form = DTMLFile('dtml/lampadas_cvs_form',globals())

    _security.declareProtected('Lampadas CVS File Actions',      'manage_lampadasForm')
    manage_lampadasForm     = DTMLFile('dtml/lampadas_cvs',globals())

    # CMF ATTRIBUTES

    portal_type = 'CVS File'
    set = _security.setPermissionDefault
    set('Edit CVS File', ('Owner', 'Manager', 'Authenticated'))
    set('FTP Access', ('Owner', 'Manager', 'Authenticated'))
    set('Create CVS File', ('Owner', 'Manager'))
    set('Move CVS File', ('Owner', 'Manager'))
    set('Add CVSFile comment', ('Owner', 'Manager', 'Authenticated'))
    set = None

    def inCMF(self):
        """Return true if this object is in a CMF portal.
        """
        return hasattr(self.aq_inner.aq_parent,'portal_membership')
    
    _security.declarePublic('getId')
    def getId(self):
        try: return self.id()
        except TypeError: return self.id
    
    _security.declareProtected('View CVS File', 'SearchableText')
    def SearchableText(self):
        return self.getContents()

    def setFileInfo(self, filepath='', title='', description=''):
        """Sets meta-data from the CVS properties screen.
        """
        self.filepath = filepath
        self.title = title
        self.description = description

# register security information
Globals.InitializeClass(PloneCVSFile)
