#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class Language(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            return self.dms.document.get_by_keys([['lang', '=', self.code]])
        elif attribute=='i18n':
            self.i18n = self.dms.language_i18n.get_by_keys([['lang_code', '=', self.code]])
            return self.i18n
        elif attribute=='name':
            name = LampadasCollection()
            for key in self.i18n.keys():
                i18n = self.i18n[key]
                name[i18n.lang] = i18n.name
            return name
        else:
            raise AttributeError('No such attribute %s' % attribute)
