#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class Topic(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            self.documents = self.dms.document_topic.get_by_keys([['topic_code', '=', self.code]])
            return self.documents
        elif attribute=='parent':
            self.parent = self.dms.topic.get_by_id(self.parent_code)
            return self.parent
        elif attribute=='children':
            self.children = self.dms.topic.get_by_keys([['parent_code', '=', self.code]])
            return self.children
        elif attribute=='title':
            parent = self.parent
            if parent:
                title = LampadasCollection()
                for key in parent.title.keys():
                    title[key] = parent.title[key]
                for key in self.name.keys():
                    title[key] = title[key] + ': ' + self.name[key]
            else:
                title = self.name
            self.title = title
            return self.title
        elif attribute in ('name', 'description'):
            name = LampadasCollection()
            description = LampadasCollection()
            i18ns = self.dms.topic_i18n.get_by_keys([['topic_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                name[i18n.lang] = i18n.topic_name
                description[i18n.lang] = i18n.topic_desc
            if attribute=='name':
                return name
            else:
                return description
        else:
            raise AttributeError('No such attribute %s' % attribute)
