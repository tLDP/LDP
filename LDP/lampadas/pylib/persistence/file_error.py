#!/usr/bin/python

from base import Persistence

class FileError(Persistence):

    def __getattr__(self, attribute):
        if attribute=='sourcefile':
            return self.dms.sourcefile.get_by_id(self.filename)
        elif attribute=='error':
            return self.dms.error.get_by_id(self.err_id)
        else:
            raise AttributeError('No such attribute %s' % attribute)
