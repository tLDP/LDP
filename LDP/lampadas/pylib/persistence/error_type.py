#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class ErrorType(Persistence):

    def __getattr__(self, attribute):
        if attribute=='errors':
            return self.dms.error.get_by_keys([['err_type_code', '=', self.code]])

        if attribute in ('name', 'description'):
            self.name = LampadasCollection()
            self.description = LampadasCollection()
            i18ns = self.dms.error_type_i18n.get_by_keys([['err_type_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                self.name[i18n.lang] = i18n.err_type_name
                self.description[i18n.lang] = i18n.err_type_desc
        if attribute=='name':
            return self.name
        else:
            return self.description

