#!/usr/bin/python

from base import Persistence

class DocumentCollection(Persistence):

    def __getattr__(self, attribute):
        if attribute=='collection':
            return self.dms.collection.get_by_id(self.collection_code)
        elif attribute=='document':
            return self.dms.document.get_by_id(self.doc_id)
        else:
            raise AttributeError('No such attribute %s' % attribute)
