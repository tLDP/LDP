from Globals import YES, NO
from base import DataManager

class DocumentCollection(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'document_collection',
            {'doc_id':              {'key_field': YES, 'data_type': 'int',      'nullable': NO,  'i18n': NO,  'foreign_key': 'document.doc_id'},
             'collection_code':     {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'collection.collection_code'},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})
