#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class Collection(Persistence):
    """
    Base class for persistent collections.
    """
    def __getattr__(self, attribute):
        if attribute=='documents':
            return self.dms.document_collection.get_by_keys([['collection_code', '=', self.code]])
        elif attribute in ('name', 'description'):
            name = LampadasCollection()
            description = LampadasCollection()
            i18ns = self.dms.collection_i18n.get_by_keys([['collection_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                name[i18n.lang] = i18n.collection_name
                description[i18n.lang] = i18n.collection_desc
            if attribute=='name':
                return name
            elif attribute=='description':
                return description
        else:
            raise AttributeError('No such attribute %s' % attribute)

