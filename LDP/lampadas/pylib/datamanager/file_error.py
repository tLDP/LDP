from Globals import YES, NO
from base import DataManager

class FileError(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'file_error',
            {'filename':            {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'sourcefile.filename'},
             'err_id':              {'key_field': YES, 'data_type': 'int',      'nullable': NO,  'i18n': NO,  'foreign_key': 'error.err_id'},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})
