#!/usr/bin/python

from Config import config
from base import Persistence
from Globals import trim

class Username(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            return self.dms.document_user.get_by_keys([['username', '=', self.username]])
        elif attribute=='name':
            return trim(trim(self.first_name + ' ' + self.middle_name) + ' ' + self.surname)
        else:
            raise AttributeError('No such attribute %s' % attribute)

    def can_edit(self, doc_id=None, username=None, news_id=None, page_code=None, string_code=None):

        # Sysadmin can do anything
        if self.sysadmin > 0:
            return 1

        if not doc_id==None:
            if self.docs.has_key(doc_id):
                return 1
            if self.admin==1:
                return 1
            if doc_id==0:
                return config.user_can_add_doc
                    
        if not page_code==None:
            if self.admin==1:
                if page_code=='':
                    return config.admin_can_add_page
                else:
                    return config.admin_can_edit_page
                
        if not string_code==None:
            if self.admin==1:
                if string_code=='':
                    return config.admin_can_add_string
                else:
                    return config.admin_can_edit_string

        if not username==None:
            if username==self.username:
                return 1
            elif self.admin==1:
                if user_code=='':
                    return config.admin_can_add_user
                else:
                    return config.admin_can_edit_user

        return 0
