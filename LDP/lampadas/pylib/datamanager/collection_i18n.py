from Globals import YES, NO
from base import DataManager

class CollectionI18n(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'collection_i18n',
            {'collection_code':     {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'collection.collection_code', 'attribute': 'code'},
             'lang':                {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'language.lang_code'},
             'collection_name':     {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': YES, 'foreign_key': '', 'attribute': 'name'},
             'collection_desc':     {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': YES, 'foreign_key': '', 'attribute': 'description'},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': YES, 'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': YES, 'foreign_key': ''}})
