#!/usr/bin/python

from base import Persistence

class Session(Persistence):

    def __getattr__(self, attribute):
        if attribute=='user':
            self.user = self.dms.username.get_by_id(self.username)
            return self.user
        else:
            raise AttributeError('No such attribute %s' % attribute)

