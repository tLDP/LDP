#!/usr/bin/python

from base import Persistence

class DocumentFile(Persistence):

    def __getattr__(self, attribute):
        if attribute=='document':
            self.document = self.dms.document.get_by_id(self.doc_id)
            return self.document
        elif attribute=='sourcefile':
            self.sourcefile = self.dms.sourcefile.get_by_id(self.doc_id)
            return self.sourcefile
        else:
            raise AttributeError('No such attribute %s' % attribute)
