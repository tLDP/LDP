#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class Section(Persistence):

    def __getattr__(self, attribute):
        if attribute=='pages':
            return self.dms.page.get_by_keys([['section_code', '=', self.code]])

        if attribute in ('name',):
            self.name = LampadasCollection()
            i18ns = self.dms.section_i18n.get_by_keys([['section_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                self.name[i18n.lang] = i18n.section_name
        if attribute=='name':
            return self.name

