#!/usr/bin/python

from base import Persistence

class Document(Persistence):
    """
    Base class for a persistent document.
    """

    def __getattr__(self, attribute):
        if attribute=='collections':
            return self.dms.document_collection.get_by_keys([['doc_id', '=', self.id]])
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
        elif attribute=='language':
            return self.dms.language.get_by_id(self.lang)
        elif attribute=='license':
            return self.dms.license.get_by_id(self.license_code)
        elif attribute=='top_file':
            top_file = self.dms.document_file.get_by_keys([['doc_id', '=', self.id], ['top', '=', 1]])
            if top_file.count()==1:
                return top_file[top_file.keys()[0]].sourcefile
            else:
                return None
        elif attribute=='file_error_count':
            count = 0
            for key in self.files.keys():
                docfile = self.files[key]
                sourcefile = docfile.sourcefile
                count = count + sourcefile.errors.count()
            return count
        else:
            raise AttributeError('No such attribute %s' % attribute)

    def delete(self):
        self.collections.clear()
        self.errors.clear()
        self.files.clear()
        self.notes.clear()
        self.ratings.clear()
        self.versions.clear()
        self.topics.clear()
        self.users.clear()
        self.dm.delete(self)
        
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
