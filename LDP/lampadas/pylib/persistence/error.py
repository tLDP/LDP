#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class Error(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            return self.dms.document_error.get_by_keys([['err_id', '=', self.id]])

        if attribute in ('name', 'description'):
            self.name = LampadasCollection()
            self.description = LampadasCollection()
            i18ns = self.dms.error_i18n.get_by_keys([['err_id', '=', self.id]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                self.name[i18n.lang] = i18n.error_name
                self.description[i18n.lang] = i18n.error_desc
        if attribute=='name':
            return self.name
        else:
            return self.description

