from Globals import YES, NO
from base import DataManager

class LanguageI18n(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'language_i18n',
            {'lang_code':           {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': '', 'attribute': 'code'},
             'lang':                {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'language.lang_code'},
             'lang_name':           {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': YES, 'foreign_key': '', 'attribute': 'name'},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': YES, 'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': YES, 'foreign_key': ''}})
