
from Globals import InitializeClass
from Products.OMFDefault import DublinCoreImpl

class OMF(DublinCoreImpl):
    """Mix-in class that provides OMF metadata, based on Dublin Core.
    """

    def __init__(self, 
                 title = '',
                 subject = (),
                 description = '',
                 contributors = (),
                 effective_date = None,
                 expiration_date = None,
                 format = 'text/html',
                 language = '',
                 rights = ''
                 ):
        DublinCoreImpl.__init__(self,
                                title,
                                subject,
                                description,
                                contributors,
                                effective_date,
                                expiration_date,
                                format,
                                language,
                                rights)
        self._editMetadata(title,
                           subject,
                           description,
                           contributors,
                           effective_date,
                           expiration_date,
                           format,
                           language,
                           rights)

InitializeClass(OMF)

