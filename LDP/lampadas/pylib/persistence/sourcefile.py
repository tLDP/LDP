#!/usr/bin/python

from base import Persistence

class Sourcefile(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            return self.dms.document_file.get_by_keys([['sourcefile', '=', self.filename]])
        if attribute=='errors':
            return self.dms.file_error.get_by_keys([['sourcefile', '=', self.filename]])
