#!/usr/bin/python

from base import Persistence

class CollectionI18n(Persistence):
    
    def __str__(self):
        return 'persistence.CollectionI18n: %s/%s' % (self.code, self.lang)
