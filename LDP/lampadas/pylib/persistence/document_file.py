#!/usr/bin/python

from base import Persistence

class DocumentFile(Persistence):

    def __getattr__(self, attribute):
        if attribute=='document':
            return self.dms.document.get_by_id(self.doc_id)
        elif attribute=='sourcefile':
            return self.dms.sourcefile.get_by_id(self.filename)
        else:
            raise AttributeError('No such attribute %s' % attribute)
