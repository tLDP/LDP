from Globals import YES, NO
from base import DataManager
        
class Log(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'log',
            {'level':               {'key_field': NO,  'data_type': 'int',      'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'username':            {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': 'username.username'},
             'message':             {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'doc_id':              {'key_field': NO,  'data_type': 'int',      'nullable': YES, 'i18n': NO,  'foreign_key': 'document.doc_id'},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})
