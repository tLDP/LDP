#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class Role(Persistence):

    def __getattr__(self, attribute):
        if attribute=='users':
            return dms.document_user.get_by_keys([['role_code', '=', self.code]])
        elif attribute=='i18n':
            self.i18n = self.dms.role_i18n.get_by_keys([['code', '=', self.code]])
            return self.i18n
        elif attribute=='name':
            name = LampadasCollection()
            for key in self.i18n.keys():
                i18n = self.i18n[key]
                name[i18n.lang] = i18n.name
            return name
        elif attribute=='description':
            description = LampadasCollection()
            for key in self.i18n.keys():
                i18n = self.i18n[key]
                description[i18n.lang] = i18n.description
            return description
        else:
            raise AttributeError('No such attribute %s' % attribute)
