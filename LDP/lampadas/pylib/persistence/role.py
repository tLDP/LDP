#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class Role(Persistence):

    def __getattr__(self, attribute):
        if attribute=='users':
            return dms.document_user.get_by_keys([['role_code', '=', self.code]])
        elif attribute in ('name', 'description'):
            name = LampadasCollection()
            description = LampadasCollection()
            i18ns = self.dms.role_i18n.get_by_keys([['role_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                name[i18n.lang] = i18n.role_name
                description[i18n.lang] = i18n.role_desc
            if attribute=='name':
                return name
            else:
                return description
        else:
            raise AttributeError('No such attribute %s' % attribute)
