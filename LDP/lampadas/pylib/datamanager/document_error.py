from Globals import YES, NO
from base import DataManager

class DocumentError(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'document_error',
            {'doc_id':              {'key_field': YES, 'data_type': 'int',      'nullable': NO,  'i18n': NO,  'foreign_key': 'document.doc_id'},
             'err_id':              {'key_field': YES, 'data_type': 'int',      'nullable': NO,  'i18n': NO,  'foreign_key': 'error.err_id'},
             'notes':               {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})
