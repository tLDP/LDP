#!/usr/bin/python
# 
# This file is part of the Lampadas Documentation System.
# 
# Copyright (c) 2000, 2001, 2002 David Merrill <david@lupercalia.net>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 
# SourceFiles

from Globals import *
from Config import config
from BaseClasses import *
from Database import db
from sqlgen import sqlgen
import os
import re


#FIXME: Read these from a text file, so they can be tweaked
# w/o code changes.

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


class SourceFiles(LampadasCollection):
    """
    A collection object of all source files.
    """
    
    def load(self):
        sql = 'SELECT filename, filesize, filemode, format_code, dtd_code, dtd_version, title, abstract, version, pub_date, isbn, encoding, created, updated FROM sourcefile'
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            sourcefile = SourceFile()
            sourcefile.load_row(row)
            sourcefile.errors = FileErrs(sourcefile.filename)
            self.data[sourcefile.filename] = sourcefile
        # FIXME: use cursor.execute(sql,params) instead! --nico
        self.load_file_errors()

    def load_file_errors(self):
        sql = 'SELECT filename, err_id, date_entered FROM file_error'
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            filename = trim(row[0])
            fileerr = FileErr()
            fileerr.load_row(row)
            self[filename].errors[fileerr.err_id] = fileerr

    def add(self, filename, format_code='', dtd_code='', dtd_version='', title='', abstract='', version='', pub_date='', isbn='', encoding=''):
        sql = 'INSERT INTO sourcefile(filename, format_code, dtd_code, dtd_version, title, abstract, version, pub_date, isbn, encoding) VALUES (' + wsq(filename) + ', ' + wsq(format_code) + ', ' + wsq(dtd_code) + ', ' + wsq(dtd_version) + ', ' + wsq(title) + ', ' + wsq(abstract) + ', ' + wsq(version) + ', ' + wsq(pub_date) + ', ' + wsq(isbn) + ', ' + wsq(encoding) + ')'
        db.runsql(sql)
        sourcefile = SourceFile(filename)
        sourcefile.errors.filename = filename
        sourcefile.calc_filenames()
    	sourcefile.read_metadata()
        self.data[filename] = sourcefile
        return sourcefile

    def delete(self, filename):
        sourcefile = self[filename]
        sourcefile.errors.clear()
        sql = 'DELETE FROM sourcefile WHERE fiename=' + wsq(filename)
        db.runsql(sql)
        db.commit()
        del self.data[filename]
        
class SourceFile:
    """
    A file on the filesystem or on the network via http or ftp.
    """

    def __init__(self, filename=''):
        self.filename         = filename
        self.filesize         = 0
        self.filemode         = 0
        self.format_code      = ''
        self.dtd_code         = ''
        self.dtd_version      = ''
        self.title            = ''
        self.abstract         = ''
        self.version          = ''
        self.pub_date         = ''
        self.isbn             = ''
        self.encoding         = ''
        self.created          = ''
        self.updated          = ''
        self.basename         = ''
        self.dbsgmlfile       = ''
        self.xmlfile          = ''
        self.utfxmlfile       = ''
        self.utftempxmlfile   = ''
        self.tidyxmlfile      = ''
        self.htmlfile         = ''
        self.indexfile        = ''
        self.txtfile          = ''
        self.omffile          = ''
        self.calc_filenames()
        self.errors = FileErrs()
        self.errors.filename = filename
        if filename > '':
            self.load()

    def load(self):
        sql = 'SELECT filename, filesize, filemode, format_code, dtd_code, dtd_version, title, abstract, version, pub_date, isbn, encoding, created, updated FROM sourcefile WHERE filename=' + wsq(self.filename)
        cursor = db.select(sql)
        row = cursor.fetchone()
        if not row==None:
            self.load_row(row)
            self.errors = FileErrs(self.filename)

    def load_row(self, row):
        self.filename    = trim(row[0])
        self.filesize    = safeint(row[1])
        self.filemode    = safeint(row[2])
        self.format_code = trim(row[3])
        self.dtd_code    = trim(row[4])
        self.dtd_version = trim(row[5])
        self.title       = trim(row[6])
        self.abstract    = trim(row[7])
        self.version     = trim(row[8])
        self.pub_date    = trim(row[9])
        self.isbn        = trim(row[10])
        self.encoding    = trim(row[11])
        self.created     = time2str(row[12])
        self.updated     = time2str(row[13])
        self.errors.filename = self.filename
        self.calc_filenames()
        
        # Always update the meta-data as soon as it is read.
        self.read_metadata()

    def save(self):
        dict = {'filename':self.filename,
                'filesize':999,             # FIXME: Actually write the value! (I'm getting an error.)
                'filemode':self.filemode,
                'format_code':self.format_code,
                'dtd_code':self.dtd_code,
                'dtd_version':self.dtd_version,
                'title':self.title,
                'abstract':self.abstract,
                'version':self.version,
                'pub_date':self.pub_date,
                'isbn':self.isbn,
                'encoding':self.encoding,
                'created':self.created,
                'updated':self.updated
                }
        sql = sqlgen.update('sourcefile',dict,['filename'])
        db.execute(sql,dict)
        db.commit()

    def calc_filenames(self):
        self.file_only	 = os.path.split(self.filename)[1]
        self.basename	 = os.path.splitext(self.file_only)[0]
        if self.filename[:7]=='http://' or self.filename[:6]=='ftp://':
            self.local = 0
            self.localname = ''
            self.in_cvs = 0
        else:
            self.local = 1
            if self.filename[:7]=='file://':
                self.in_cvs = 0
                self.localname = self.filename[7:]
            else:
                self.in_cvs = 1
                self.localname = config.cvs_root + self.filename
        self.dbsgmlfile     = self.basename + '.db.sgml'
        self.xmlfile        = self.basename + '.xml'
        self.utfxmlfile     = self.basename + '.utf.xml'
        self.utftempxmlfile = self.basename + '.utf.temp.xml'
        self.tidyxmlfile    = self.basename + '.tidy.xml'
        self.htmlfile       = self.basename + '.html'
        self.indexfile      = 'index.html'
        self.txtfile        = self.basename + '.txt'
        self.omffile        = self.basename + '.omf'

    def read_metadata(self):
        """
        Attempts to read meta-data from a source file.
        Currently, it reads DocBook, LinuxDoc and WikiText files,
        but it can be extended to read from Texinfo and
        possibly other formats as well.
        """

        # Use these to store the new values.
        # We'll compare it later and save only if something has changed.
        format_code = ''
        dtd_code    = ''
        dtd_version = ''
        title       = ''
        abstract    = ''
        version     = ''
        pub_date    = ''
        isbn        = ''
        encoding    = ''
      
        # Determine file format.
        extension = string.lower(string.split(self.filename, '.')[-1])
        if EXTENSIONS.has_key(extension) > 0:
            format_code = EXTENSIONS[extension]
        else:
            format_code = ''

        # FIXME: Use libxml2's Python bindings to do this,
        # or at least use a Python library. This parsing
        # is a cheap and dirty (not to mention ugly) kludge.

        # Determine DTD for SGML and XML files
        if format_code not in METADATA_FORMATS:
            dtd_code    = 'none'

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
            if format_code=='wikitext':
                dtd_code    ='docbook'

            # Look for DocType declaration
            m = re.search('DOCTYPE(.*?)>', header, flags)
            if m:
                doctype = m.group(1)

                # Look for DocBook declaration
                m = re.search('DOCBOOK(.*)', doctype, flags)
                if m:
                    m = re.search('.*?(V.*?)\/\/', doctype, flags)
                    if m: dtd_version = trim(m.group(1))
                else:

                    # Look for LinuxDoc declaration
                    m = re.search('LINUXDOC(.*)', doctype, flags)
                    if m:
                        doctype = m.group(1)
                        m = re.search('.*?LINUXDOC\s*?(.*?)\/\/', doctype, flags)
                        if m: dtd_version = trim(m.group(1))

            m = re.search('<TITLE>(.*?)</TITLE>', header, flags)
            if m:
                title = m.group(1)

            m = re.search('<ABSTRACT>(.*?)</ABSTRACT>', header, flags)
            if m:
                abstract = m.group(1)

            if dtd_code=='docbook':
                m = re.search('<PUBDATE>(.*?)</PUBDATE>', header, flags)
                if m:
                    pub_date = m.group(1)
            elif dtd_code=='linuxdoc':
                m = re.search('<VERSION>(.*?)</VERSION>', header, flags)
                if m:
                    version = m.group(1)
                m = re.search('<DATE>(.*?)</DATE>', header, flags)
                if m:
                    pub_date = m.group(1)
            
            m = re.search('<ISBN>(.*?)</ISBN>', header, flags)
            if m:
                isbn = m.group(1)

            m = re.search("ENCODING='(.*?)'", header, flags)
            if m:
                encoding = m.group(1)
            else:
                m = re.search('ENCODING="(.*?)"', header, flags)
                if m:
                    encoding = m.group(1)
                
        # Decide whether we need to save this data
        if format_code  <> self.format_code or \
           dtd_code     <> self.dtd_code or \
           dtd_version  <> self.dtd_version or \
           title        <> self.title or \
           abstract     <> self.abstract or \
           version      <> self.version or \
           pub_date     <> self.pub_date or \
           isbn         <> self.isbn or \
           encoding     <> self.encoding:
            updated = 1
        else:
            updated = 0

        self.format_code = format_code
        self.dtd_code    = dtd_code
        self.dtd_version = dtd_version
        self.title       = title
        self.abstract    = abstract
        self.version     = version
        self.pub_date    = pub_date
        self.isbn        = isbn
        self.encoding    = encoding

        if updated==1:
            self.save()

# FileErrs

class FileErrs(LampadasCollection):
    """
    A collection object providing access to all file errors, as identified by the
    Lintadas subsystem.
    """

    def __init__(self, filename=''):
        self.data = {}
        self.filename = filename
        if filename > '':
            self.load()

    def load(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "SELECT filename, err_id, date_entered FROM file_error WHERE filename=" + wsq(self.filename)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            file_err = FileErr()
            file_err.load_row(row)
            self.data[file_err.err_id] = file_err

    def clear(self):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "DELETE FROM file_error WHERE filename=" + wsq(self.filename)
        db.runsql(sql)
        db.commit()
        self.data = {}

    def count(self):
        return len(self)
        
# FIXME: Try instantiating a FileErr object, then adding it to the *document*
# rather than passing all these parameters here. --nico

    def add(self, err_id):
        # FIXME: use cursor.execute(sql,params) instead! --nico
        sql = "INSERT INTO file_error(filename, err_id) VALUES (" + wsq(self.filename) + ", " + str(err_id) + ')'
        assert db.runsql(sql)==1
        file_err = FileErr()
        file_err.filename = self.filename
        file_err.err_id = err_id
        file_err.date_entered = now_string()
        self.data[file_err.err_id] = file_err
        db.commit()

class FileErr:
    """
    An error filed against a document by the Lintadas subsystem.
    """

    def __init__(self, filename=''):
        self.filename = filename
        if filename=='': return
        self.load()

    def load(self):
        sql = 'SELECT filename, err_id, date_entered FROM file_error WHERE filename=' + wsq(self.filename)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            self.load_row(row)
    
    def load_row(self, row):
        self.filename     = trim(row[0])
        self.err_id       = safeint(row[1])
        self.date_entered = time2str(row[2])


sourcefiles = SourceFiles()
sourcefiles.load()

