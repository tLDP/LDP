#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class Section(Persistence):

    def __getattr__(self, attribute):
        if attribute=='pages':
            self.pages = self.dms.page.get_by_keys([['section_code', '=', self.code]])
            return self.pages
        elif attribute=='static_count':
            self.nonstatic_count = self.pages.count([['only_dynamic', '=', 0]])
            return self.nonstatic_count
        elif attribute=='nonregistered_count':
            self.nonregistered_count = self.pages.count([['only_registered', '=', 0]])
            return self.nonregistered_count
        elif attribute=='nonadmin_count':
            self.nonadmin_count = self.pages.count([['only_admin', '=', 0]])
            return self.nonadmin_count
        elif attribute=='nonsysadmin_count':
            self.nonsysadmin_count = self.pages.count([['only_sysadmin', '=', 0]])
            return self.nonsysadmin_count
        elif attribute=='name':
            name = LampadasCollection()
            i18ns = self.dms.section_i18n.get_by_keys([['section_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                name[i18n.lang] = i18n.section_name
            return name
        else:
            raise AttributeError('No such attribute %s' % attribute)
