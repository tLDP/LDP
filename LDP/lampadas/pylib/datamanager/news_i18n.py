from Globals import YES, NO
from base import DataManager

class NewsI18n(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'news_i18n',
            {'news_id':             {'key_field': YES, 'data_type': 'int',      'nullable': NO,  'i18n': NO,  'foreign_key': 'news.news_id', 'attribute': 'id'},
             'lang':                {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'language.lang_code'},
             'version':             {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': YES, 'foreign_key': ''},
             'headline':            {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': YES, 'foreign_key': ''},
             'news':                {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': YES, 'foreign_key': ''},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': YES, 'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': YES, 'foreign_key': ''}})
