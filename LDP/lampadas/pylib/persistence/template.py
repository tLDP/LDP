#!/usr/bin/python

from base import Persistence

class Template(Persistence):

    def __getattr__(self, attribute):
        if attribute=='pages':
            self.pages = self.dms.page.get_by_keys([['template_code', '=', self.code]])
            return self.pages
        else:
            raise AttributeError('No such attribute %s' % attribute)

