#!/usr/bin/python

from base import Persistence

class DocumentFile(Persistence):

    def __getattr__(self, attribute):
        if attribute=='document':
            return self.dms.document.get_by_id(self.doc_id)
        if attribute=='file':
            return self.dms.sourcefile.get_by_id(self.doc_id)
