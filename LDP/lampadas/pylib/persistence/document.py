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

    def update_metadata(self):
        topfile = self.top_file
        if topfile:
            if self.title=='':       self.title       = topfile.title
            if self.format_code=='': self.format_code = topfile.format_code
            if self.dtd_code=='':    self.dtd_code    = topfile.dtd_code
            if self.dtd_version=='': self.dtd_version = topfile.dtd_version
            if self.abstract=='':    self.abstract    = topfile.abstract
            if self.version=='':     self.version     = topfile.version
            if self.pub_date=='':    self.pub_date    = topfile.pub_date
            if self.isbn=='':        self.isbn        = topfile.isbn
            if self.encoding=='':    self.encoding    = topfile.encoding
