from Globals import YES, NO
from base import DataManager

class FormatI18n(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'format_i18n',
            {'format_code':         {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'format.format_code', 'attribute': 'code'},
             'lang':                {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'language.lang_code'},
             'format_name':         {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': YES, 'foreign_key': '', 'attribute': 'name'},
             'format_desc':         {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': YES, 'foreign_key': '', 'attribute': 'description'},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': YES,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': YES,  'foreign_key': ''}})
