from Globals import YES, NO
from base import DataManager

class DocumentUser(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'document_user',
            {'doc_id':              {'key_field': YES, 'data_type': 'int',      'nullable': NO,  'i18n': NO,  'foreign_key': 'document.doc_id',   'foreign_attr': 'users'},
             'username':            {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'username.username', 'foreign_attr': 'documents'},
             'role_code':           {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'role.role_code'},
             'email':               {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'active':              {'key_field': NO,  'data_type': 'bool',     'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})
