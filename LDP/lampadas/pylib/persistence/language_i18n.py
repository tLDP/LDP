#!/usr/bin/python

from base import Persistence

class LanguageI18n(Persistence):

    def __str__(self):
        return 'persistence.LanguageI18n: %s/%s' % (self.code, self.lang)

