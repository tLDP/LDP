from Globals import YES, NO
from base import DataManager

class Sourcefile(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'sourcefile',
            {'filename':            {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'filesize':            {'key_field': NO,  'data_type': 'int',      'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'filemode':            {'key_field': NO,  'data_type': 'int',      'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'format_code':         {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': 'format.format_code'},
             'dtd_code':            {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': 'dtd.dtd_code'},
             'dtd_version':         {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'title':               {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'abstract':            {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'version':             {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'pub_date':            {'key_field': NO,  'data_type': 'date',     'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'isbn':                {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': ''},
             'encoding':            {'key_field': NO,  'data_type': 'string',   'nullable': YES, 'i18n': NO,  'foreign_key': 'encoding.encoding'},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})
