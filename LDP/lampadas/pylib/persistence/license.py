#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class License(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            self.documents = self.dms.document.get_by_keys([['license_code', '=', self.code]])
            return self.documents
        elif attribute in ('short_name', 'name', 'description'):
            self.short_name = LampadasCollection()
            self.name = LampadasCollection()
            self.description = LampadasCollection()
            i18ns = self.dms.license_i18n.get_by_keys([['license_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                self.short_name[i18n.lang] = i18n.license_short_name
                self.name[i18n.lang] = i18n.license_name
                self.description[i18n.lang] = i18n.license_desc
            if attribute=='short_name':
                return self.short_name
            elif attribute=='name':
                return self.name
            else:
                return self.description
        else:
            raise AttributeError('No such attribute %s' % attribute)
