from Globals import YES, NO
from base import DataManager

class Encoding(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'encoding',
            {'encoding':            {'key_field': YES, 'data_type': 'string',   'nullable': NO, 'i18n': NO,  'foreign_key': 'encoding.encoding'},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})
