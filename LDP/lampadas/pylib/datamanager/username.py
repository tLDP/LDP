from Globals import YES, NO
from base import DataManager
        
class Username(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'username',
            {'username':            {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'session_id':          {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'first_name':          {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'middle_name':         {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'surname':             {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'email':               {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'admin':               {'key_field': NO,  'data_type': 'bool',     'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'sysadmin':            {'key_field': NO,  'data_type': 'bool',     'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'password':            {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'password':            {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'notes':               {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})
