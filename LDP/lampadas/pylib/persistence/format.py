#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class Format(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            self.documents = self.dms.document.get_by_keys([['format_code', '=', self.code]])
            return self.documents
        elif attribute in ('name', 'description'):
            self.name = LampadasCollection()
            self.description = LampadasCollection()
            i18ns = self.dms.format_i18n.get_by_keys([['format_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                self.name[i18n.lang] = i18n.format_name
                self.description[i18n.lang] = i18n.format_desc
            if attribute=='name':
                return self.name
            else:
                return self.description
        else:
            raise AttributeError('No such attribute %s' % attribute)
