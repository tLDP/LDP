#!/usr/bin/python

from Globals import *
from Config import config
from base import Persistence
import os
import string
import re

# This is a list of file extensions and the file types
# they represent.
EXTENSIONS = {
    'sgml': 'sgml',
    'xml':  'xml',
    'wt':   'wikitext',
    'txt':  'text',
    'texi': 'texinfo',
    'sh':   'shell',
}

METADATA_FORMATS = ('sgml', 'xml', 'wikitext')

class Sourcefile(Persistence):

    def __getattr__(self, attribute):
        if attribute=='documents':
            return self.dms.document_file.get_by_keys([['filename', '=', self.filename]])
        elif attribute=='errors':
            return self.dms.file_error.get_by_keys([['filename', '=', self.filename]])
        elif attribute=='dtd':
            return self.dms.dtd.get_by_id(self.dtd_code)
        elif attribute=='format':
            return self.dms.format.get_by_id(self.format_code)
        elif attribute=='local':
            return not (self.filename[:7]=='http://' or self.filename[:6]=='ftp://')
        elif attribute=='localname':
            filename = self.filename
            if filename[:7]=='http://' or filename[:6]=='ftp://':
                return ''
            else:
                if filename[:7]=='file://':
                    return filename[7:]
                else:
                    return config.cvs_root + self.filename
        elif attribute=='in_cvs':
            if self.local==0:
                return 0
            else:
                if self.filename[:7]=='file://':
                    return 0
                else:
                    return 1 
        elif attribute=='file_only':
            return os.path.split(self.filename)[1]
        elif attribute=='basename':
            return os.path.splitext(self.file_only)[0]
        elif attribute=='dbsgmlfile':
            return self.basename + '.db.sgml'
        elif attribute=='xmlfile':
            return self.basename + '.xml'
        elif attribute=='utfxmlfile':
            return self.basename + '.utf.xml'
        elif attribute=='utftempxmlfile':
            return self.basename + '.utf.temp.xml'
        elif attribute=='tidyxmlfile':
            return self.basename + '.tidy.xml'
        elif attribute=='htmlfile':
            return self.basename + '.html'
        elif attribute=='indexfile':
            return 'index.html'
        elif attribute=='txtfile':
            return self.basename + '.txt'
        elif attribute=='omffile':
            return self.basename + '.omf'
        else:
            raise AttributeError('No such attribute %s' % attribute)
    
    def read_metadata(self):
        """
        Attempts to read meta-data from a source file.
        Currently, it reads DocBook, LinuxDoc and WikiText files,
        but it can be extended to read from Texinfo and
        possibly other formats as well.
        """

        # Determine file format.
        extension = string.lower(string.split(self.filename, '.')[-1])
        if EXTENSIONS.has_key(extension) > 0:
            self.format_code = EXTENSIONS[extension]
        else:
            self.format_code = ''

        # FIXME: Use libxml2's Python bindings to do this,
        # or at least use a Python library. This parsing
        # is a cheap and dirty (not to mention ugly) kludge.

        # Determine DTD for SGML and XML files
        if self.format_code not in METADATA_FORMATS:
            self.dtd_code    = 'none'

        elif self.local==1:
        
            try:
                fh = open(self.localname, 'r')
            except IOError:
                return
            
            flags = re.I | re.M | re.S

            # Read the document header
            header = WOStringIO()
            while (1):
                line = fh.readline()
                header.write(line)
                
                # Stop at the end of the header or EOF.
                if re.search('</ARTICLEINFO>', line, flags): break
                if re.search('</ARTHEADER>', line, flags): break
                if re.search('<SECT', line, flags): break
                if line=='':    break
            fh.close()

            # Convert header into a regular string for searching
            header = header.get_value()

            # WikiText is *always* DocBook, whether or not it contains
            # an explicit DocType declaration.
            if self.format_code=='wikitext':
                self.dtd_code    ='docbook'

            # Look for DocType declaration
            m = re.search('DOCTYPE(.*?)>', header, flags)
            if m:
                doctype = trim(m.group(1))

                # Look for DocBook declaration
                m = re.search('DOCBOOK(.*)', doctype, flags)
                if m:
                    self.dtd_code = 'docbook'
                    m = re.search('.*?(V.*?)\/\/', doctype, flags)
                    if m: dtd_version = trim(m.group(1))
                else:

                    # Look for LinuxDoc declaration
                    m = re.search('LINUXDOC(.*)', doctype, flags)
                    if m:
                        self.dtd_code = 'linuxdoc'
                        doctype = trim(m.group(1))
                        m = re.search('(.*?)\/\/', doctype, flags)
                        if m: self.dtd_version = trim(m.group(1))
                        else:
                            m = re.search('(.*?)\[', doctype, flags)
                            if m: self.dtd_version = trim(m.group(1))
                            else: self.dtd_version = trim(doctype)

            m = re.search('<TITLE>(.*?)</TITLE>', header, flags)
            if m:
                self.title = trim(m.group(1))

            m = re.search('<ABSTRACT>(.*?)</ABSTRACT>', header, flags)
            if m:
                self.abstract = trim(m.group(1))

            if self.dtd_code=='docbook':
                m = re.search('<PUBDATE>(.*?)</PUBDATE>', header, flags)
                if m:
                    self.pub_date = trim(m.group(1))
            elif self.dtd_code=='linuxdoc':
                m = re.search('<VERSION>(.*?)</VERSION>', header, flags)
                if m:
                    self.version = trim(m.group(1))
                m = re.search('<DATE>(.*?)</DATE>', header, flags)
                if m:
                    self.pub_date = trim(m.group(1))
            
            m = re.search('<ISBN>(.*?)</ISBN>', header, flags)
            if m:
                self.isbn = trim(m.group(1))

            m = re.search("ENCODING='(.*?)'", header, flags)
            if m:
                self.encoding = trim(m.group(1)).upper()
            else:
                m = re.search('ENCODING="(.*?)"', header, flags)
                if m:
                    self.encoding = trim(m.group(1)).upper()
