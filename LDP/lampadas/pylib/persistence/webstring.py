#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class WebString(Persistence):

    def __getattr__(self, attribute):
        if attribute in ('string', 'version'):
            self.string = LampadasCollection()
            self.version = LampadasCollection()
            i18ns = self.dms.webstring_i18n.get_by_keys([['string_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                self.string[i18n.lang] = i18n.string
                self.version[i18n.lang] = i18n.version
        if attribute=='string':
            return self.string
        else:
            return self.version

