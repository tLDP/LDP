#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class Topic(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            return self.dms.document_topic.get_by_keys([['topic_code', '=', self.code]])
        elif attribute=='parent':
            return self.dms.topic.get_by_id(self.parent_code)
        elif attribute=='children':
            return self.dms.topic.get_by_keys([['parent_code', '=', self.code]])
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
            return title
        elif attribute=='i18n':
            self.i18n = self.dms.topic_i18n.get_by_keys([['code', '=', self.code]])
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
