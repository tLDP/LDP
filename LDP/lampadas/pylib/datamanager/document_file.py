from Globals import YES, NO
from base import DataManager

class DocumentFile(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'document_file',
            {'doc_id':              {'key_field': YES, 'data_type': 'int',      'nullable': NO,  'i18n': NO,  'foreign_key': 'document.doc_id'},
             'filename':            {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'sourcefile.filename'},
             'top':                 {'key_field': NO,  'data_type': 'bool',     'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})
