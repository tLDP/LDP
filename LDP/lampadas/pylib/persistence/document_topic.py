#!/usr/bin/python

from base import Persistence

class DocumentTopic(Persistence):

    def __getattr__(self, attribute):
        if attribute=='document':
            return self.dms.document.get_by_id(self.doc_id)
        elif attribute=='topic':
            return self.dms.topic.get_by_id(self.topic_code)

