#!/usr/bin/python

from base import Persistence

class Document(Persistence):
    """
    Base class for a persistent document.
    """

    def __getattr__(self, attribute):
        if attribute=='collections':
            return self.dms.collection.get_by_keys([['doc_id', '=', self.id]])
        elif attribute=='errors':
            return self.dms.document_error.get_by_keys([['doc_id', '=', self.id]])
        elif attribute=='files':
            return self.dms.document_file.get_by_keys([['doc_id', '=', self.id]])
        elif attribute=='notes':
            return self.dms.document_note.get_by_keys([['doc_id', '=', self.id]])
        elif attribute=='ratings':
            return self.dms.document_rating.get_by_keys([['doc_id', '=', self.id]])
        elif attribute=='versions':
            return self.dms.document_rev.get_by_keys([['doc_id', '=', self.id]])
        elif attribute=='topics':
            return self.dms.document_topic.get_by_keys([['doc_id', '=', self.id]])
        elif attribute=='users':
            return self.dms.document_user.get_by_keys([['doc_id', '=', self.id]])
        else:
            raise AttributeError('No such attribute %s' % attribute)
