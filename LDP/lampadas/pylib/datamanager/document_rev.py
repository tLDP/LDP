from Globals import YES, NO
from base import DataManager

class DocumentRev(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'document_rev',
            {'rev_id':              {'key_field': YES, 'data_type': 'sequence', 'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'doc_id':              {'key_field': NO,  'data_type': 'int',      'nullable': NO,  'i18n': NO,  'foreign_key': 'document.doc_id'},
             'version':             {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'pub_date':            {'key_field': NO,  'data_type': 'date',     'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'initials':            {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'notes':               {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})
