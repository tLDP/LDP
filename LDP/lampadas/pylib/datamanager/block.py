from Globals import YES, NO
from base import DataManager
       
class Block(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'block',
            {'block_code':          {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': '', 'attribute': 'code'},
             'block':               {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})

