#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class PubStatus(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            return self.dms.document.get_by_keys([['pub_status_code', '=', self.code]])
        elif attribute in ('name', 'description'):
            name = LampadasCollection()
            description = LampadasCollection()
            i18ns = self.dms.pub_status_i18n.get_by_keys([['pub_status_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                name[i18n.lang] = i18n.pub_status_name
                description[i18n.lang] = i18n.pub_status_desc
            if attribute=='name':
                return name
            else:
                return description
        else:
            raise AttributeError('No such attribute %s' % attribute)
