#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class License(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            return self.dms.document.get_by_keys([['license_code', '=', self.code]])
        elif attribute in ('short_name', 'name', 'description'):
            short_name = LampadasCollection()
            name = LampadasCollection()
            description = LampadasCollection()
            i18ns = self.dms.license_i18n.get_by_keys([['license_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                short_name[i18n.lang] = i18n.license_short_name
                name[i18n.lang] = i18n.license_name
                description[i18n.lang] = i18n.license_desc
            if attribute=='short_name':
                return short_name
            elif attribute=='name':
                return name
            else:
                return description
        else:
            raise AttributeError('No such attribute %s' % attribute)
