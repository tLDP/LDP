"""
I am an extension of CVSFile that adds Plone functionality.
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
from Products.CVSFile.CVSFile import CVSFile, manage_add, manage_add_with_upload
from Products.CVSFile.ICVSFile import ICVSFile

# Python builtins
import os

################################################################
# Container Methods
################################################################

# globals() is standard python for passing the current namespace
manage_addForm       = Globals.DTMLFile('dtml/create',               globals())
cvsregistry_formpart = DTMLFile('dtml/cvsregistry_formpart', globals())
cvssandbox_formpart  = DTMLFile('dtml/cvssandbox_formpart',  globals())

#def manage_add(self,
#               id, title, description, 
#               target_filepath, basedir='', REQUEST=None):
#    """Factory method to actually create an instance of PloneCVSFile.
#    """
#    CVSFile.manage_add(self,
#               id, title, description, 
#               target_filepath, basedir, REQUEST)
#
#def manage_add_with_upload(self,
#                           id, title, description,
#                           target_filepath, upload_file, basedir,
#                           REQUEST=None):
#    """Factory method to actually create an instance of PloneCVSFile.
#    """
#    CVSFile.manage_add_with_upload(self,
#                           id, title, description,
#                           target_filepath, upload_file, basedir,
#                           REQUEST)

################################################################
# CVSFile class
################################################################

class PloneCVSFile(CVSFile):

    """Extended from CVSFile
    """

    meta_type = 'Plone CVS File'  # This is the name Zope will use for the Product in
                                  # the "addProduct" list

    __implements__ = ICVSFile

    # This tuple defines a dictionary for each tab in the management interface
    # label = label of tab, action = url it links to
    manage_options = ExternalFile.manage_options + (
	{'label':'CVS',	    'action': 'manage_cvsForm'},
        )

    _security = ClassSecurityInfo()

    # set security for the object itself, e.g. if it is accessed in DTML code
    # This line is REQUIRED to allow access to CVSFiles by the public (ariel DTDs, etc.)
    _security.declareObjectPublic()

    # call __call__() method on DTMLFile for our edit form, point at our cvs_form.dtml
    # globals() is standard python for passing the current namespace
    cvs_form           = DTMLFile('dtml/cvs_form',globals())
    
    _security.declareProtected('Manage Plone CVS Files',      'manage_cvsForm')
    manage_cvsForm     = DTMLFile('dtml/cvs',globals())

    # these lines exist so we can call them from DTML
    cvsregistry_formpart = cvsregistry_formpart
    cvssandbox_formpart  = cvssandbox_formpart
    # end of DTML scoping hack

# register security information
Globals.InitializeClass(PloneCVSFile)
