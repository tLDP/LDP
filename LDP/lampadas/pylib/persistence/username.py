#!/usr/bin/python

from base import Persistence
from Globals import trim

class Username(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            self.documents = self.dms.document_user.get_by_keys([['username', '=', self.username]])
            return self.documents
        elif attribute=='name':
            return trim(trim(self.first_name + ' ' + self.middle_name) + ' ' + self.surname)
        else:
            raise AttributeError('No such attribute %s' % attribute)
