#!/usr/bin/python

from base import Persistence

class DocumentUser(Persistence):

    def __getattr__(self, attribute):
        if attribute=='document':
            self.document = self.dms.document.get_by_id(self.doc_id)
            return self.document
        elif attribute=='user':
            self.user = self.dms.username.get_by_id(self.username)
            return self.user
        elif hasattr(self.document, attribute):
            return getattr(self.document, attribute)
        elif hasattr(self.user, attribute):
            return getattr(self.user, attribute)
        else:
            raise AttributeError('No such attribute %s' % attribute)
