from Globals import YES, NO
from base import DataManager

class News(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'news',
            {'news_id':             {'key_field': YES, 'data_type': 'sequence', 'nullable': NO,  'i18n': NO,  'foreign_key': '', 'attribute': 'id'},
             'pub_date':            {'key_field': NO,  'data_type': 'date',     'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})
