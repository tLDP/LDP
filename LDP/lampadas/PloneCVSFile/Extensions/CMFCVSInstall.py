"""
CMF CVSFile Installation script

This was shamelessly copied from ZWiki's insatllation script,
then modified to suit my needs.

This file is an installation script for CFM CVSFile.  It's meant to be
used as an External Method.  To use, add an external method to the
root of the CMF Site that you want CMF CVSFile registered in with the
configuration:

 id:            cmf_cvs_install
 title:         
 module name:   PloneCVSFile.CMFInstall
 function name: install

Then go to the management screen for the newly added external method
and click the 'Test' tab.  The install function will execute and give
information about the steps it took.
"""

from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.PloneCVSFile import factory_type_information
from Products.CMFCore.TypesTool import ContentFactoryMetadata
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.PloneCVSFile import cmf_cvsfile_globals
from Products.PloneCVSFile.Defaults import META_TYPE, PORTAL_TYPE
from ZODB.PersistentMapping import PersistentMapping
import string

def install(self):
    """
    Register CMF CVS File with portal_types and friends.
    """
    out = StringIO()
    typestool = getToolByName(self, 'portal_types')
    skinstool = getToolByName(self, 'portal_skins')
    workflowtool = getToolByName(self, 'portal_workflow')

    out.write('factory_type_information:\n')
    out.write(str(factory_type_information))
    
    # Borrowed from CMFDefault.Portal.PortalGenerator.setupTypes()
    # We loop through anything defined in the factory type information
    # and configure it in the types tool if it doesn't already exist
    for t in factory_type_information:
        if t['id'] not in typestool.objectIds():
            cfm = apply(ContentFactoryMetadata, (), t)
            typestool._setObject(t['id'], cfm)
            out.write('Registered %s with the types tool\n' % t['id'])
        else:
            out.write('Object "%s" already existed in the types tool\n' % (
                t['id']))

     # Setup the skins
     # This is borrowed from CMFDefault/scripts/addImagesToSkinPaths.pys
    if 'lampadas' not in skinstool.objectIds():
        # We need to add Filesystem Directory Views for any directories
        # in our skins/ directory.  These directories should already be
        # configured.
        addDirectoryViews(skinstool, 'skins', cmf_cvsfile_globals)
        out.write("Added 'lampadas' directory view to portal_skins\n")

    # Now we need to go through the skin configurations and insert
    # 'wiki' into the configurations.  Preferably, this should be
    # right before where 'content' is placed.  Otherwise, we append
    # it to the end.
    skins = skinstool.getSkinSelections()
    for skin in skins:
        path = skinstool.getSkinPath(skin)
        path = map(string.strip, string.split(path,','))
        for dir in ( 'lampadas_templates', ):

            if not dir in path:
                try:
                    idx = path.index( 'custom' )
                except ValueError:
                    idx = 999
                path.insert( idx+1, dir )

        path = string.join(path, ', ')
        # addSkinSelection will replace existing skins as well.
        skinstool.addSkinSelection(skin, path)
        out.write("Added custom skin to %s skin\n" % skin)

# Commenting this out. Looks like we want to set up
# a default workflow, not clear it away.
#
#    # remove workflow for Wiki pages
#    cbt = workflowtool._chains_by_type
#    if cbt is None:
#        cbt = PersistentMapping()
#    cbt[META_TYPE] = []
#    cbt[PORTAL_TYPE] = []
#    workflowtool._chains_by_type = cbt
#    out.write("Established new workflows for Lampadas objects")
    return out.getvalue()
