#!/usr/bin/python

from base import Persistence

class FileError(Persistence):

    def __getattr__(self, attribute):
        if attribute=='sourcefile':
            self.sourcefile = self.dms.sourcefile.get_by_id(self.filename)
            return self.sourcefile
        elif attribute=='error':
            self.error = self.dms.error.get_by_id(self.err_id)
            return self.error
        else:
            raise AttributeError('No such attribute %s' % attribute)
