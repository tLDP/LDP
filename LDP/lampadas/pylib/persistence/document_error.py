#!/usr/bin/python

from base import Persistence

class DocumentError(Persistence):

    def __getattr__(self, attribute):
        if attribute=='document':
            return self.dms.document.get_by_id(self.doc_id)
        elif attribute=='error':
            return self.dms.error.get_by_id(self.err_id)
        elif attribute=='err_type_code':
            return self.error.err_type_code
        else:
            raise AttributeError('No such attribute %s' % attribute)
