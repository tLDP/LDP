#!/usr/bin/python

from base import Persistence

class DocumentUser(Persistence):

    def __getattr__(self, attribute):
        if attribute=='document':
            return self.dms.document.get_by_id(self.doc_id)
        elif attribute=='user':
            return self.dms.username.get_by_id(self.username)
        else:
            raise AttributeError('No such attribute %s' % attribute)
