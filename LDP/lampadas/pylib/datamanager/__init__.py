"""
This package provides a querying interface to the back end database.

Every table in the database has a corresponding data manager class here
that handles the details of querying, inserting, saving, loading and
deleting data for that table. Of course, most of these classes don't
really implement anything directly, because almost all normal operations
can be handled through the DataManager superclass.

There is no caching on this data, but a cache is planned.

To use these classes, instantiate a single instance of the DataManagers()
collection, which will automatically contain a reference to one of each
type of data manager. Before using it, assign the data managers with the
classes it should use to instantiate objects by calling set_object_classes()
and passing it in the name of the package which contains them. To use the
base persistence classes, call se_object_classes(persistence).
"""

from datamanager.datamanagers import DataManagers

# Load the various modules' classes here for convenience.
#from datamanager.block              import Block
#from datamanager.collection         import Collection
#from datamanager.collection_i18n    import CollectionI18n
#from datamanager.document           import Document
#from datamanager.document_error     import DocumentError
#from datamanager.document_file      import DocumentFile
#from datamanager.document_note      import DocumentNote
#from datamanager.document_rating    import DocumentRating
#from datamanager.document_rev       import DocumentRev
#from datamanager.document_topic     import DocumentTopic
#from datamanager.document_user      import DocumentUser
#from datamanager.dtd                import DTD
#from datamanager.dtd_i18n           import DTDI18n
#from datamanager.encoding           import Encoding
#from datamanager.error              import Error
#from datamanager.error_i18n         import ErrorI18n
#from datamanager.error_type         import ErrorType
#from datamanager.error_type_i18n    import ErrorTypeI18n
#from datamanager.file_error         import FileError
#from datamanager.file_report        import FileReport
#from datamanager.file_report_i18n   import FileReportI18n
#from datamanager.format             import Format
#from datamanager.format_i18n        import FormatI18n
#from datamanager.language           import Language
#from datamanager.language_i18n      import LanguageI18n
#from datamanager.license            import License
#from datamanager.license_i18n       import LicenseI18n
#from datamanager.log                import Log
#from datamanager.news               import News
#from datamanager.news_i18n          import NewsI18n
#from datamanager.page               import Page
#from datamanager.page_i18n          import PageI18n
#from datamanager.pub_status         import PubStatus
#from datamanager.pub_status_i18n    import PubStatusI18n
#from datamanager.review_status      import ReviewStatus
#from datamanager.review_status_i18n import ReviewStatusI18n
#from datamanager.role               import Role
#from datamanager.role_i18n          import RoleI18n
#from datamanager.section            import Section
#from datamanager.section_i18n       import SectionI18n
#from datamanager.session            import Session
#from datamanager.sourcefile         import Sourcefile
#from datamanager.template           import Template
#from datamanager.topic              import Topic
#from datamanager.topic_i18n         import TopicI18n
#from datamanager.type               import Type
#from datamanager.type_i18n          import TypeI18n
#from datamanager.username           import Username
#from datamanager.webstring          import WebString
#from datamanager.webstring_i18n     import WebStringI18n
