#!/usr/bin/python

from base import Persistence

class DocumentTopic(Persistence):

    def __getattr__(self, attribute):
        if attribute=='document':
            self.document = self.dms.document.get_by_id(self.doc_id)
            return self.document
        elif attribute=='topic':
            self.topic = self.dms.topic.get_by_id(self.topic_code)
            return self.topic
        elif attribute=='sort_order':
            self.sort_order =self.topic.sort_order
            return self.sort_order
        else:
            raise AttributeError('No such attribute %s' % attribute)
