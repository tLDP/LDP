#!/usr/bin/python

from base import Persistence
import os
from Config import config

class Sourcefile(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            self.documents = self.dms.document_file.get_by_keys([['sourcefile', '=', self.filename]])
            return self.documents
        elif attribute=='errors':
            self.errors = self.dms.file_error.get_by_keys([['sourcefile', '=', self.filename]])
            return self.errors
        elif attribute=='dtd':
            self.dtd = self.dms.dtd.get_by_id(self.dtd_code)
            return self.dtd
        elif attribute=='format':
            self.format = self.dms.format.get_by_id(self.format_code)
            return self.format
        elif attribute=='local':
            self.local = not (self.filename[:7]=='http://' or self.filename[:6]=='ftp://')
            return self.local
        elif attribute=='localname':
            if self.filename[:7]=='http://' or self.filename[:6]=='ftp://':
                self.localname = ''
            else:
                if self.filename[:7]=='file://':
                    self.localname = self.filename[7:]
                else:
                    self.localname = config.cvs_root + self.filename
            return self.localname
        elif attribute=='in_cvs':
            if self.local==0:
                self.in_cvs = 0
            else:
                if self.filename[:7]=='file://':
                    self.in_cvs = 0
                else:
                    self.in_cvs = 1
            return self.in_cvs
        elif attribute=='file_only':
            self.file_only = os.path.split(self.filename)[1]
            return self.file_only
        elif attribute=='basename':
            self.basename = os.path.splitext(self.file_only)[0]
            return self.basename
        elif attribute=='dbsgmlfile':
            self.dbsgmlfile = self.basename + '.db.sgml'
            return self.dbsgmlfile
        elif attribute=='xmlfile':
            self.xmlfile = self.basename + '.xml'
            return self.xmlfile
        elif attribute=='utfxmlfile':
            self.utfxmlfile = self.basename + '.utf.xml'
            return self.utfxmlfile
        elif attribute=='utftempxmlfile':
            self.utftempxmlfile = self.basename + '.utf.temp.xml'
            return self.utftempxmlfile
        elif attribute=='tidyxmlfile':
            self.tidyxmlfile = self.basename + '.tidy.xml'
            return self.tidyxmlfile
        elif attribute=='htmlfile':
            self.htmlfile = self.basename + '.html'
            return self.htmlfile
        elif attribute=='indexfile':
            self.indexfile = 'index.html'
            return self.indexfile
        elif attribute=='txtfile':
            self.txtfile = self.basename + '.txt'
            return self.txtfile
        elif attribute=='omffile':
            self.omffile = self.basename + '.omf'
            return self.omffile
        else:
            raise AttributeError('No such attribute %s' % attribute)
