
from Globals import InitializeClass
from Products.CMFDefault.DublinCore import DefaultDublinCoreImpl
from Products.CMFDefault.utils import tuplize, semi_split
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo

class OMF(DefaultDublinCoreImpl):
    """Mix-in class that provides OMF metadata, based on Dublin Core.
    """

    security = ClassSecurityInfo()

    def __init__(self, 
                 title = '',
                 subject = (),          # These are like Lampadas Topics
                 description = '',      # DocBook abstract
                 contributors = (),     # other contributors
                 effective_date = None, # publication date
                 expiration_date = None,
                 format = 'text/html',  # mime type
                 language = '',         # ISO code, 2 characters
                 rights = '',           # License code
                 authors = (),
                 maintainers = (),      # Owner, by default
                 versions = (),         # identifier, date, description tuples
                 types = (),            # HOWTO, FAQ, etc.
                 formats = (),          # DTD, Mime tuple
                 identifiers = (),      # Scrollkeeper ID
                 sources = (),          # http://www.lampadas.org
                 relations = (),        # A related document's identifier
                 coverages = ()         # geographic, distribution, kernel, architecture, os tuples
                 ):
        self._editMetadata(title,
                           subject,
                           description,
                           contributors,
                           effective_date,
                           expiration_date,
                           format,
                           language,
                           rights,
                           authors,
                           maintainers,
                           versions,
                           types,
                           formats,
                           identifiers,
                           sources,
                           relations,
                           coverages)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, '_editMetadata')
    def _editMetadata(self,
                      title,
                      subject,
                      description,
                      contributors,
                      effective_date,
                      expiration_date,
                      format,
                      language,
                      rights,
                      authors,
                      maintainers,
                      versions,
                      types,
                      formats,
                      identifiers,
                      sources,
                      relations,
                      coverages):
        """Update all editable meta-data for this resource."""
        self.setTitle(title)
        self.setSubject(subject)
        self.setDescription(description)
        self.setContributors(contributors)
        self.setEffectiveDate(effective_date)
        self.setExpirationDate(expiration_date)
        self.setFormat(format)
        self.setLanguage(language)
        self.setRights(rights)
        self.setAuthors(authors)
        self.setMaintainers(maintainers)
        self.setVersions(versions)
        self.setTypes(types)
        self.setFormats(formats)
        self.setIdentifiers(identifiers)
        self.setSources(sources)
        self.setRelations(relations)
        self.setCoverages(coverages)

    security.declarePublic('Authors')
    def Authors(self):
        """OMF Author elements - resource creator
           (already implemented in DublinCore, but not well enough).
        """
        return self.authors

    security.declarePublic('Maintainers')
    def Maintainers(self):
        """OMF maintainers."""
        return self.maintainers

    security.declarePublic('Versions')
    def Versions(self):
        """OMF version tags."""
        return self.versions

    security.declarePublic('Types')
    def Types(self):
        """OMF type tags."""
        return self.types

    security.declarePublic('Formats')
    def Formats(self):
        """OMF Format tuples."""
        return self.formats

    security.declarePublic('Identifiers')
    def Identifiers(self):
        """OMF identifiers (unique ids)."""
        return self.identifiers

    security.declarePublic('Sources')
    def Sources(self):
        """OMF Source (publisher, source of the doc.)"""
        return self.sources

    security.declarePublic('Relations')
    def Relations(self):
        """OMF Relations -- related document identifiers."""
        return self.relations

    security.declarePublic('Coverages')
    def Coverages(self):
        """OMF coverages -- geographic, os, kernel, arch, etc."""
        return self.coverages

    security.declarePublic('getMetadataHeaders')
    def getMetadataHeaders(self):
        """Return RFC-822-style headers."""
        hdrlist = []
        hdrlist.append( ( 'Title', self.Title() ) )
        hdrlist.append( ( 'Subject', string.join( self.Subject(), ', ' ) ) )
        hdrlist.append( ( 'Publisher', self.Publisher() ) )
        hdrlist.append( ( 'Description', self.Description() ) )
        hdrlist.append( ( 'Contributors', string.join(
            self.Contributors(), '; ' ) ) )
        hdrlist.append( ( 'Effective_date', self.EffectiveDate() ) )
        hdrlist.append( ( 'Expiration_date', self.ExpirationDate() ) )
        hdrlist.append( ( 'Type', self.Type() ) )
        hdrlist.append( ( 'Format', self.Format() ) )
        hdrlist.append( ( 'Language', self.Language() ) )
        hdrlist.append( ( 'Rights', self.Rights() ) )
        hdrlist.append( ( 'Authors', self.Authors() ) )
        hdrlist.append( ( 'Maintainers', self.Maintainers() ) )
        hdrlist.append( ( 'Versions', self.Versions() ) )
        hdrlist.append( ( 'Types', self.Types() ) )
        hdrlist.append( ( 'Formats', self.Formats() ) )
        hdrlist.append( ( 'Identifiers', self.Identifiers() ) )
        hdrlist.append( ( 'Sources', self.Sources() ) )
        hdrlist.append( ( 'Relations', self.Relations() ) )
        hdrlist.append( ( 'Coverages', self.Coverages() ) )
        return hdrlist
    
    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setAuthors')
    def setAuthors(self, authors):
        """OMF creator elements."""
        self.authors = tuplize('authors', authors, semi_split)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setMaintainers')
    def setMaintainers(self, maintainers):
        """OMF maintainer elements."""
        self.maintainers = tuplize('maintainers', maintainers, semi_split)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setVersions')
    def setVersions(self, versions):
        """OMF version elements."""
        self.versions = tuplize('versions', versions, semi_split)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setTypes')
    def setTypes(self, types):
        """OMF type elements."""
        self.types = tuplize('types', types, semi_split)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setFormats')
    def setFormats(self, formats):
        """OMF format elements."""
        self.formats = tuplize('formats', formats, semi_split)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setIdentifiers')
    def setIdentifiers(self, identifiers):
        """OMF identifier elements."""
        self.identifiers = tuplize('identifiers', identifiers, semi_split)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setSources')
    def setSources(self, sources):
        """OMF source elements."""
        self.sources = tuplize('sources', sources, semi_split)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setRelations')
    def setRelations(self, relations):
        """OMF relation elements."""
        self.relations = tuplize('relations', relations, semi_split)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'setCoverages')
    def setCoverages(self, coverages):
        """OMF coverage elements."""
        self.coverages = tuplize('coverages', coverages, semi_split)

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'manage_editMetadata')
    def manage_editMetadata(self, 
                            title,
                            subject,
                            description,
                            contributors,
                            effective_date,
                            expiration_date,
                            format,
                            language,
                            rights,
                            authors,
                            maintainers,
                            versions,
                            types,
                            formats,
                            identifiers,
                            sources,
                            relations,
                            coverages,
                            REQUEST):
        """Update meta-data from the ZMI."""
        self._editMetadata(title,
                           subject,
                           description,
                           contributors,
                           effective_date,
                           expiration_date,
                           format,
                           language,
                           rights,
                           authors,
                           maintainers,
                           versions,
                           types,
                           formats,
                           identifiers,
                           sources,
                           relations,
                           coverages)
        REQUEST['RESPONSE'].redirect(self.absolute_url()
                            + '/manage_metadata'
                            + '?manage_tabs_message=Metadata+updated.')

    security.declareProtected(CMFCorePermissions.ModifyPortalContent, 'edit_Metadata')
    def edit_Metadata(self,
                      title = '',
                      subject = (),
                      description = '',
                      contributors = (),
                      effective_date = None,
                      expiration_date = None,
                      format = 'text/html',
                      language = '',
                      rights = '',
                      authors = (),
                      maintainers = (),
                      versions = (),
                      types = (),
                      formats = (),
                      identifiers = (),
                      sources = (),
                      relations = (),
                      coverages = ()
                      ):
        """Required for WebDAV support."""
        self.failIfLocked()
        self._editMetadata(title            = title,
                           subject          = subject,
                           description      = description,
                           contributors     = contributors,
                           effective_date   = effective_date,
                           expiration_date  = expiration_date,
                           format           = format,
                           language         = language,
                           rights           = rights,
                           authors          = authors,
                           maintainers      = maintainers,
                           versions         = versions,
                           types            = types,
                           formats          = formats,
                           identifiers      = identifiers,
                           sources          = sources,
                           relations        = relations,
                           coverages        = coverages
                           )
        self.reindexObject()
    
InitializeClass(OMF)

