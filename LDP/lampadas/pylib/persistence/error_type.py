#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class ErrorType(Persistence):

    def __getattr__(self, attribute):
        if attribute=='errors':
            return self.dms.error.get_by_keys([['err_type_code', '=', self.code]])
        elif attribute=='i18n':
            self.i18n = self.dms.error_type_i18n.get_by_keys([['err_type_code', '=', self.code]])
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
