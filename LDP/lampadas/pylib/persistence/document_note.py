#!/usr/bin/python

from base import Persistence

class DocumentNote(Persistence):

    def __getattr__(self, attribute):
        if attribute=='document':
            return self.dms.document.get_by_id(self.doc_id)
        else:
            raise AttributeError('No such attribute %s' % attribute)
