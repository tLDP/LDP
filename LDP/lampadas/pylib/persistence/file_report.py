#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class FileReport(Persistence):

    def __getattr__(self, attribute):
        if attribute in ('name', 'description'):
            self.name = LampadasCollection()
            self.description = LampadasCollection()
            i18ns = self.dms.file_report_i18n.get_by_keys([['report_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                self.name[i18n.lang] = i18n.report_name
                self.description[i18n.lang] = i18n.report_desc
        if attribute=='name':
            return self.name
        else:
            return self.description

