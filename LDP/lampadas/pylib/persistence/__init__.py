"""
This package provides base classes for persistent objects.
It relies on the datamanager package to do the actual database work.

These objects don't have a lot of functionality -- they only exist
so they can be subclassed elsewhere to provide role-specific behaviors.
"""

# Load the various modules' classes here for convenience.
from persistence.block               import Block
from persistence.collection          import Collection
from persistence.collection_i18n     import CollectionI18n
from persistence.document            import Document
from persistence.document_collection import DocumentCollection
from persistence.document_error      import DocumentError
from persistence.document_file       import DocumentFile
from persistence.document_note       import DocumentNote
from persistence.document_rating     import DocumentRating
from persistence.document_rev        import DocumentRev
from persistence.document_topic      import DocumentTopic
from persistence.document_user       import DocumentUser
from persistence.dtd                 import DTD
from persistence.dtd_i18n            import DTDI18n
from persistence.encoding            import Encoding
from persistence.error               import Error
from persistence.error_i18n          import ErrorI18n
from persistence.error_type          import ErrorType
from persistence.error_type_i18n     import ErrorTypeI18n
from persistence.file_error          import FileError
from persistence.file_report         import FileReport
from persistence.file_report_i18n    import FileReportI18n
from persistence.format              import Format
from persistence.format_i18n         import FormatI18n
from persistence.language            import Language
from persistence.language_i18n       import LanguageI18n
from persistence.license             import License
from persistence.license_i18n        import LicenseI18n
from persistence.log                 import Log
from persistence.news                import News
from persistence.news_i18n           import NewsI18n
from persistence.page                import Page
from persistence.page_i18n           import PageI18n
from persistence.pub_status          import PubStatus
from persistence.pub_status_i18n     import PubStatusI18n
from persistence.review_status       import ReviewStatus
from persistence.review_status_i18n  import ReviewStatusI18n
from persistence.role                import Role
from persistence.role_i18n           import RoleI18n
from persistence.section             import Section
from persistence.section_i18n        import SectionI18n
from persistence.session             import Session
from persistence.sourcefile          import Sourcefile
from persistence.template            import Template
from persistence.topic               import Topic
from persistence.topic_i18n          import TopicI18n
from persistence.type                import Type
from persistence.type_i18n           import TypeI18n
from persistence.username            import Username
from persistence.webstring           import WebString
from persistence.webstring_i18n      import WebStringI18n
