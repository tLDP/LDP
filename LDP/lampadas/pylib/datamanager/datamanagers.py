#!/usr/bin/python

"""
A collection of datamanagers, one for each table.
"""

from BaseClasses import LampadasCollection

# Load the various modules' classes here for convenience.
from datamanager.block               import Block
from datamanager.collection          import Collection
from datamanager.collection_i18n     import CollectionI18n
from datamanager.document            import Document
from datamanager.document_collection import DocumentCollection
from datamanager.document_error      import DocumentError
from datamanager.document_file       import DocumentFile
from datamanager.document_note       import DocumentNote
from datamanager.document_rating     import DocumentRating
from datamanager.document_rev        import DocumentRev
from datamanager.document_topic      import DocumentTopic
from datamanager.document_user       import DocumentUser
from datamanager.dtd                 import DTD
from datamanager.dtd_i18n            import DTDI18n
from datamanager.encoding            import Encoding
from datamanager.error               import Error
from datamanager.error_i18n          import ErrorI18n
from datamanager.error_type          import ErrorType
from datamanager.error_type_i18n     import ErrorTypeI18n
from datamanager.file_error          import FileError
from datamanager.file_report         import FileReport
from datamanager.file_report_i18n    import FileReportI18n
from datamanager.format              import Format
from datamanager.format_i18n         import FormatI18n
from datamanager.language            import Language
from datamanager.language_i18n       import LanguageI18n
from datamanager.license             import License
from datamanager.license_i18n        import LicenseI18n
from datamanager.log                 import Log
from datamanager.news                import News
from datamanager.news_i18n           import NewsI18n
from datamanager.page                import Page
from datamanager.page_i18n           import PageI18n
from datamanager.pub_status          import PubStatus
from datamanager.pub_status_i18n     import PubStatusI18n
from datamanager.review_status       import ReviewStatus
from datamanager.review_status_i18n  import ReviewStatusI18n
from datamanager.role                import Role
from datamanager.role_i18n           import RoleI18n
from datamanager.section             import Section
from datamanager.section_i18n        import SectionI18n
from datamanager.session             import Session
from datamanager.sourcefile          import Sourcefile
from datamanager.template            import Template
from datamanager.topic               import Topic
from datamanager.topic_i18n          import TopicI18n
from datamanager.type                import Type
from datamanager.type_i18n           import TypeI18n
from datamanager.username            import Username
from datamanager.webstring           import WebString
from datamanager.webstring_i18n      import WebStringI18n

class DataManagers(LampadasCollection):
    """
    A collection of the available data managers.
    """

    def __init__(self):
        LampadasCollection.__init__(self)
        self['block']               = Block()
        self['collection']          = Collection()
        self['collection_i18n']     = CollectionI18n()
        self['document']            = Document()
        self['document_collection'] = DocumentCollection()
        self['document_error']      = DocumentError()
        self['document_file']       = DocumentFile()
        self['document_note']       = DocumentNote()
        self['document_rating']     = DocumentRating()
        self['document_rev']        = DocumentRev()
        self['document_topic']      = DocumentTopic()
        self['document_user']       = DocumentUser()
        self['dtd']                 = DTD()
        self['dtd_i18n']            = DTDI18n()
        self['encoding']            = Encoding()
        self['error']               = Error()
        self['error_i18n']          = ErrorI18n()
        self['error_type']          = ErrorType()
        self['error_type_i18n']     = ErrorTypeI18n()
        self['file_error']          = FileError()
        self['file_report']         = FileReport()
        self['file_report_i18n']    = FileReportI18n()
        self['format']              = Format()
        self['format_i18n']         = FormatI18n()
        self['language']            = Language()
        self['language_i18n']       = LanguageI18n()
        self['license']             = License()
        self['license_i18n']        = LicenseI18n()
        self['log']                 = Log()
        self['news']                = News()
        self['news_i18n']           = NewsI18n()
        self['page']                = Page()
        self['page_i18n']           = PageI18n()
        self['pub_status']          = PubStatus()
        self['pub_status_i18n']     = PubStatusI18n()
        self['review_status']       = ReviewStatus()
        self['review_status_i18n']  = ReviewStatusI18n()
        self['role']                = Role()
        self['role_i18n']           = RoleI18n()
        self['section']             = Section()
        self['section_i18n']        = SectionI18n()
        self['session']             = Session()
        self['sourcefile']          = Sourcefile()
        self['template']            = Template()
        self['topic']               = Topic()
        self['topic_i18n']          = TopicI18n()
        self['type']                = Type()
        self['type_i18n']           = TypeI18n()
        self['username']            = Username()
        self['webstring']           = WebString()
        self['webstring_i18n']      = WebStringI18n()

        # Point each data manager back here. The data managers will in turn
        # point all objects they create back here.:w
        for key in self.keys():
            self[key].dms = self

    def set_object_classes(self, persistence):
        """
        Tells the datamanagers in this collection what classes to use when
        instantiating new objects.

        It expects to be passed a reference to the persistence class, or
        some subclass of it.
        """
        
        self['block'].object_class               = persistence.Block
        self['collection'].object_class          = persistence.Collection
        self['collection_i18n'].object_class     = persistence.CollectionI18n
        self['document'].object_class            = persistence.Document
        self['document_collection'].object_class = persistence.DocumentError
        self['document_error'].object_class      = persistence.DocumentError
        self['document_file'].object_class       = persistence.DocumentFile
        self['document_note'].object_class       = persistence.DocumentNote
        self['document_rating'].object_class     = persistence.DocumentRating
        self['document_rev'].object_class        = persistence.DocumentRev
        self['document_topic'].object_class      = persistence.DocumentTopic
        self['document_user'].object_class       = persistence.DocumentUser
        self['dtd'].object_class                 = persistence.DTD
        self['dtd_i18n'].object_class            = persistence.DTDI18n
        self['encoding'].object_class            = persistence.Encoding
        self['error'].object_class               = persistence.Error
        self['error_i18n'].object_class          = persistence.ErrorI18n
        self['error_type'].object_class          = persistence.ErrorType
        self['error_type_i18n'].object_class     = persistence.ErrorTypeI18n
        self['file_error'].object_class          = persistence.FileError
        self['file_report'].object_class         = persistence.FileReport
        self['file_report_i18n'].object_class    = persistence.FileReportI18n
        self['format'].object_class              = persistence.Format
        self['format_i18n'].object_class         = persistence.FormatI18n
        self['language'].object_class            = persistence.Language
        self['language_i18n'].object_class       = persistence.LanguageI18n
        self['license'].object_class             = persistence.License
        self['license_i18n'].object_class        = persistence.LicenseI18n
        self['log'].object_class                 = persistence.Log
        self['news'].object_class                = persistence.News
        self['news_i18n'].object_class           = persistence.NewsI18n
        self['page'].object_class                = persistence.Page
        self['page_i18n'].object_class           = persistence.PageI18n
        self['pub_status'].object_class          = persistence.PubStatus
        self['pub_status_i18n'].object_class     = persistence.PubStatusI18n
        self['review_status'].object_class       = persistence.ReviewStatus
        self['review_status_i18n'].object_class  = persistence.ReviewStatusI18n
        self['role'].object_class                = persistence.Role
        self['role_i18n'].object_class           = persistence.RoleI18n
        self['section'].object_class             = persistence.Section
        self['section_i18n'].object_class        = persistence.SectionI18n
        self['session'].object_class             = persistence.Session
        self['sourcefile'].object_class          = persistence.Sourcefile
        self['template'].object_class            = persistence.Template
        self['topic'].object_class               = persistence.Topic
        self['topic_i18n'].object_class          = persistence.TopicI18n
        self['type'].object_class                = persistence.Type
        self['type_i18n'].object_class           = persistence.TypeI18n
        self['username'].object_class            = persistence.Username
        self['webstring'].object_class           = persistence.WebString
        self['webstring_i18n'].object_class      = persistence.WebStringI18n

    def __getattr__(self, attribute):
        """
        Overrides attribute requests, and maps attribute names to collection keys.
        
        This lets you access self['block'] using the simpler syntax self.block.
        """

        return self[attribute]


