#!/usr/bin/python

from base import Persistence

class Encoding(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            return self.dms.document.get_by_keys([['encoding', '=', self.code]])
        else:
            raise AttributeError('No such attribute %s' % attribute)

