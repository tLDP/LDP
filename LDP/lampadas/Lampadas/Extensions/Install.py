#from Products.CMFTypes.Extensions.utils import installTypes
from Products.Lampadas.Extensions.utils import installTypes
from Products.Lampadas  import listTypes
from StringIO import StringIO

PKG_NAME='Lampadas'

def install(self):
    out=StringIO()

    if not hasattr(self, "_isPortalRoot"):
        print >> out, "Must be installed in a CMF Site (read Plone)"
        return
    
    print >> out, "Installing %s into %s" % (listTypes(), PKG_NAME)
        
    installTypes(self, out, listTypes(), PKG_NAME)
    print >> out, 'Successfully installed Lampadas content types.'
        
    print >> out, 'Successfully installed %s ' % PKG_NAME
        
    return out.getvalue()

