#!/usr/bin/python

from base import Persistence

class DocumentCollection(Persistence):

    def __getattr__(self, attribute):
        if attribute=='collection':
            self.collection = self.dms.collection.get_by_id(self.collection_code)
            return self.collection
        elif attribute=='document':
            self.document = self.dms.document.get_by_id(self.doc_id)
            return self.document
        else:
            raise AttributeError('No such attribute %s' % attribute)
