#!/usr/bin/python

from base import Persistence

class PageI18n(Persistence):

    def __str__(self):
        return 'persistence.PageI18n: %s/%s' % (self.code, self.lang)
