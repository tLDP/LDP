#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class Error(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            return self.dms.document_error.get_by_keys([['err_id', '=', self.id]])
        elif attribute=='error_type':
            return self.dms.error_type.get_by_id(self.err_type_code)
        elif attribute in ('name', 'description'):
            name = LampadasCollection()
            description = LampadasCollection()
            i18ns = self.dms.error_i18n.get_by_keys([['err_id', '=', self.id]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                name[i18n.lang] = i18n.err_name
                description[i18n.lang] = i18n.err_desc
            if attribute=='name':
                return name
            else:
                return description
        else:
            raise AttributeError('No such attribute %s' % attribute)
