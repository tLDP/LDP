#!/usr/bin/python

from base import Persistence

class Session(Persistence):

    def __getattr__(self, attribute):
        if attribute=='user':
            return self.dms.username.get_by_id(self.username)
        else:
            raise AttributeError('No such attribute %s' % attribute)

