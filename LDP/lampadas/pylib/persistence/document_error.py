#!/usr/bin/python

from base import Persistence

class DocumentError(Persistence):

    def __getattr__(self, attribute):
        if attribute=='document':
            self.document = self.dms.document.get_by_id(self.doc_id)
            return self.document
        elif attribute=='error':
            self.error = self.dms.error.get_by_id(self.err_id)
            return self.error
        elif attribute=='err_type_code':
            self.err_type_code = self.error.err_type_code
            return self.err_type_code
        else:
            raise AttributeError('No such attribute %s' % attribute)
