#!/usr/bin/python

from base import Persistence

class DocumentError(Persistence):

    def __getattr__(self, attribute):
        if attribute=='document':
            return self.dms.document.get_by_id(self.doc_id)
        if attribute=='error':
            return self.dms.error.get_by_id(self.doc_id)
