#!/usr/bin/python

from base import Persistence

class Username(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            return self.dms.document_user.get_by_keys([['username', '=', self.username]])
        else:
            raise AttributeError('No such attribute %s' % attribute)
