#!/usr/bin/python

from base import Persistence

class Document(Persistence):
    """
    Base class for a persistent document.
    """

    def __getattr__(self, attribute):
        if attribute=='collections':
            self.collections = self.dms.document_collection.get_by_keys([['doc_id', '=', self.id]])
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
        elif attribute=='language':
            self.language = self.dms.language.get_by_id(self.lang)
            return self.language
        elif attribute=='license':
            self.license = self.dms.license.get_by_id(self.lang)
            return self.license
        elif attribute=='top_file':
            top_file = self.dms.document_file.get_by_keys([['doc_id', '=', self.id], ['top', '=', 1]])
            if top_file.count()==1:
                self.top_file = top_file[top_file.keys()[0]].sourcefile
            else:
                self.top_file = None
            return self.top_file
        elif attribute=='file_error_count':
            count = 0
            for key in self.files.keys():
                docfile = self.files[key]
                sourcefile = docfile.sourcefile
                count = count + sourcefile.errors.count()
            self.file_error_count = count
            return self.file_error_count
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
