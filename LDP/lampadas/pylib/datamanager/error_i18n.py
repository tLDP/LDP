from Globals import YES, NO
from base import DataManager

class ErrorI18n(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'error_i18n',
            {'err_id':              {'key_field': YES, 'data_type': 'sequence', 'nullable': NO, 'i18n': NO,  'foreign_key': 'error.err_id', 'attribute': 'id'},
             'lang':                {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'language.lang_code'},
             'err_name':            {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': YES, 'foreign_key': '', 'attribute': 'name'},
             'err_desc':            {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': YES, 'foreign_key': '', 'attribute': 'description'},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': YES, 'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': YES, 'foreign_key': ''}})
