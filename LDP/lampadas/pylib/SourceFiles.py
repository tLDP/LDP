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
        sql = 'SELECT filename, format_code, filesize, filemode, modified FROM sourcefile'
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            sourcefile = SourceFile()
            sourcefile.load_row(row)
            sourcefile.errors = FileErrs(sourcefile.filename)
            self.data[sourcefile.filename] = sourcefile
        # FIXME: use cursor.execute(sql,params) instead! --nico
        self.load_file_metadata()
        self.load_file_errors()

    def load_file_metadata(self):
        sql = 'SELECT filename, dtd_code, dtd_version, title, abstract, version, pub_date, isbn, updated FROM sourcefile_metadata'
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            filename = trim(row[0])
            sourcefile = self[filename]
            sourcefile.load_metadata_row(row)

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

    def add(self, filename, format_code=''):
        sql = 'INSERT INTO sourcefile(filename, format_code) VALUES (' + wsq(filename) + ', ' + wsq(format_code) + ')'
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
        self.format_code      = ''
        self.filesize         = 0
        self.filemode         = 0
        self.modified         = ''
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
        self.reset_metadata()
        self.metadata_updated = ''
        if filename > '':
            self.load()

    def load(self):
        sql = 'SELECT filename, format_code, filesize, filemode, modified FROM sourcefile WHERE filename=' + wsq(self.filename)
        cursor = db.select(sql)
        row = cursor.fetchone()
        if not row==None:
            self.load_row(row)
            self.errors = FileErrs(self.filename)

        # Read meta-data for formats that support it.
        if self.format_code in METADATA_FORMATS:
            sql = 'SELECT filename, dtd_code, dtd_version, title, abstract, version, pub_date, isbn, updated FROM sourcefile_metadata WHERE filename=' + wsq(self.filename)
            row = cursor.fetchone()
            if not row==None:
                self.load_metadata_row(row)
            
    def load_row(self, row):
        self.filename    = trim(row[0])
        self.format_code = trim(row[1])
        self.calc_filenames()
        self.filesize    = safeint(row[2])
        self.filemode    = safeint(row[3])
        self.modified    = time2str(row[4])
        self.errors.filename = self.filename
        
        # Determine file format.
        extension = string.lower(string.split(self.filename, '.')[-1])
        if EXTENSIONS.has_key(extension) > 0:
            self.format_code = EXTENSIONS[extension]

        # Always update the meta-data as soon as it is read.
        self.read_metadata()

    def load_metadata_row(self, row):
        self.dtd_code         = trim(row[1])
        self.dtd_version      = trim(row[2])
        self.title            = trim(row[3])
        self.abstract         = trim(row[4])
        self.version          = trim(row[5])
        self.pub_date         = trim(row[6])
        self.isbn             = trim(row[7])
        self.metadata_updated = trim(row[8])
        
    def save(self):
        dict = {'format_code':self.format_code,
                'filename':self.filename,
                'filesize':999,             # FIXME: Actually write the value! (I'm getting an error.)
                'filemode':self.filemode,
                'modified':self.modified,
                }
        sql = sqlgen.update('sourcefile',dict,['filename'])
        db.execute(sql,dict)
        db.commit()
        self.save_metadata()

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

    def reset_metadata(self):
        self.dtd_code         = ''
        self.dtd_version      = ''
        self.title            = ''
        self.abstract         = ''
        self.version          = ''
        self.pub_date         = ''
        self.isbn             = ''
        self.metadata_updated = ''

    def read_metadata(self):
        """
        Attempts to read meta-data from a source file.
        Currently, it reads only DocBook and LinuxDoc files,
        but it can be extended to read from Texinfo and
        possibly other formats as well.
        """

        # FIXME: Use libxml2's Python bindings to do this,
        # or at least use a Python library. This parsing
        # is a cheap and dirty (not to mention ugly) kludge.

        # Determine DTD for SGML and XML files
        self.reset_metadata()
        if self.format_code not in METADATA_FORMATS:
            self.dtd_code = 'none'
            return
       
        try:
            fh = open(config.cvs_root + self.filename, 'r')
        except IOError:
            return
            
        # Use these to store the new data. We'll compare it later and
        # save it only if it has changed.
        dtd_code    = ''
        dtd_version = ''
        title       = ''
        abstract    = ''
        version     = ''
        pub_date    = ''
        isbn        = ''
      
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
            if line=='':
                break
        fh.close()

	# Convert header into a regular string for searching
	header = header.get_value()

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

        # Read <title>
        m = re.search('<TITLE>(.*?)</TITLE>', header, flags)
        if m: title = m.group(1)

        # Read <abstract>
        m = re.search('<ABSTRACT>(.*?)</ABSTRACT>', header, flags)
        if m: abstract = m.group(1)

        # Read <version>
        m = re.search('<VERSION>(.*?)</VERSION>', header, flags)
        if m: version = m.group(1)

        # Read <pub_date>
        m = re.search('<PUBDATE>(.*?)</PUBDATE>', header, flags)
        if m: pub_date = m.group(1)
        
        # Read <date> (LinuxDoc)
        m = re.search('<DATE>(.*?)</DATE>', header, flags)
        if m: pub_date = m.group(1)
        
        # Read <isbn> (DocBook)
        m = re.search('<ISBN>(.*?)</ISBN>', header, flags)
        if m: isbn = m.group(1)
        
        # Decide whether we need to save this data
        if dtd_code    <> self.dtd_code or \
           dtd_version <> self.dtd_version or \
           title       <> self.title or \
           abstract    <> self.abstract or \
           version     <> self.version or \
           pub_date    <> self.pub_date or \
           isbn        <> self.isbn:
            updated = 1
        else:
            updated = 0

        self.dtd_code    = dtd_code
        self.dtd_version = dtd_version
        self.title       = title
        self.abstract    = abstract
        self.version     = version
        self.pub_date    = pub_date
        self.isbn        = isbn

        if updated==1:
            self.save_metadata()
           
    def save_metadata(self):
        if self.format_code not in METADATA_FORMATS:
            return

        if db.count('sourcefile_metadata', 'filename=' + wsq(self.filename))==0:
            sql = WOStringIO('INSERT INTO sourcefile_metadata(filename, dtd_code, dtd_version, title, abstract, version, pub_date, isbn, updated) '
                             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                             % (wsq(self.filename),
                                wsq(self.dtd_code),
                                wsq(self.dtd_version),
                                wsq(self.title),
                                wsq(self.abstract),
                                wsq(self.version),
                                wsq(self.pub_date),
                                wsq(self.isbn),
                                wsq(now_string()))).get_value()
        else:
            sql = WOStringIO('UPDATE sourcefile_metadata SET dtd_code=%s, dtd_version=%s, title=%s, abstract=%s, version=%s, pub_date=%s, isbn=%s, updated=%s WHERE filename=%s'
                             % (wsq(self.dtd_code),
                                wsq(self.dtd_version),
                                wsq(self.title),
                                wsq(self.abstract),
                                wsq(self.version),
                                wsq(self.pub_date),
                                wsq(self.isbn),
                                wsq(now_string()),
                                wsq(self.filename))).get_value()
        db.runsql(sql)
        db.commit()

    def print_debug(self):
        debug = WOStringIO('Format      = %s\n'
                           'DTD         = %s\n'
                           'DTD Version = %s\n'
                           'Title       = %s\n'
                           'Abstract    = %s\n'
                           'Version     = %s\n'
                           'Pub Date    = %s\n'
                           'ISBN        = %s\n'
                           % (self.format_code,
                              self.dtd_code,
                              self.dtd_version,
                              self.title,
                              self.abstract,
                              self.version,
                              self.pub_date,
                              self.isbn))
        print debug.get_value()


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

