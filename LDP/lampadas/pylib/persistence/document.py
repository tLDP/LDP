#!/usr/bin/python

from base import Persistence

class Document(Persistence):
    """
    Base class for a persistent document.
    """

    def __getattr__(self, attribute):
        if attribute=='collections':
            self.collections = self.dms.collection.get_by_keys([['doc_id', '=', self.id]])
            return self.collections
        elif attribute=='errors':
            self.errors = self.dms.document_error.get_by_keys([['doc_id', '=', self.id]])
            return self.errors
        elif attribute=='files':
            self.files = self.dms.document_file.get_by_keys([['doc_id', '=', self.id]])
            return self.files
        elif attribute=='notes':
            self.notes =self.dms.document_note.get_by_keys([['doc_id', '=', self.id]])
            return self.notes
        elif attribute=='ratings':
            self.ratings = self.dms.document_rating.get_by_keys([['doc_id', '=', self.id]])
            return self.ratings
        elif attribute=='versions':
            self.versions = self.dms.document_rev.get_by_keys([['doc_id', '=', self.id]])
            return self.versions
        elif attribute=='topics':
            self.topics = self.dms.document_topic.get_by_keys([['doc_id', '=', self.id]])
            return self.topics
        elif attribute=='users':
            self.users = self.dms.document_user.get_by_keys([['doc_id', '=', self.id]])
            return self.users
        elif attribute=='top_file':
            self.top_file = self.dms.document_file.get_by_keys([['doc_id', '=', self.id], ['top', '=', 1]])
            return self.top_file
        else:
            raise AttributeError('No such attribute %s' % attribute)
