#!/usr/bin/python

from base import Persistence

class Encoding(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            self.documents = self.dms.document.get_by_keys([['encoding', '=', self.code]])
            return self.documents
        else:
            raise AttributeError('No such attribute %s' % attribute)

