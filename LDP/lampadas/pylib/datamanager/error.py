from Globals import YES, NO
from base import DataManager

class Error(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'error',
            {'err_id':              {'key_field': YES, 'data_type': 'sequence', 'nullable': NO, 'i18n': NO,  'foreign_key': '', 'attribute': 'id'},
             'err_type_code':       {'key_field': NO,  'data_type': 'string',   'nullable': NO, 'i18n': NO,  'foreign_key': 'error_type.err_type_code'},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})
