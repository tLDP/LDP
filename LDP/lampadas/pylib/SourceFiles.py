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

class SourceFiles(LampadasCollection):
    """
    A collection object of all source files.
    """
    
    def load(self):
        sql = 'SELECT filename, format_code, dtd_code, dtd_version, filesize, filemode, modified FROM sourcefile'
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

    def add(self, filename, format_code='', dtd_code='', dtd_version=''):
        sql = 'INSERT INTO sourcefile(filename, format_code, dtd_code, dtd_version) VALUES (' + wsq(filename) + ', ' + wsq(format_code) + ', ' + wsq(dtd_code) + ', ' + wsq(dtd_version) + ')'
        db.runsql(sql)
        sourcefile = SourceFile(filename)
        sourcefile.errors.filename = filename
        sourcefile.calc_filenames()
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
        self.filename       = filename
        self.format_code    = ''
        self.dtd_code       = ''
        self.dtd_version    = ''
        self.filesize       = 0
        self.filemode       = 0
        self.modified       = ''
        self.basename       = ''
        self.dbsgmlfile     = ''
        self.xmlfile        = ''
        self.utfxmlfile     = ''
        self.utftempxmlfile = ''
        self.tidyxmlfile    = ''
        self.htmlfile       = ''
        self.indexfile      = ''
        self.txtfile        = ''
        self.omffile        = ''
        self.calc_filenames()
        self.errors = FileErrs()
        self.errors.filename = filename
        if filename > '':
            self.load()

    def load(self):
        sql = 'SELECT filename, format_code, dtd_code, dtd_version, filesize, filemode, modified FROM sourcefile WHERE filename=' + wsq(self.filename)
        cursor = db.select(sql)
        row = cursor.fetchone()
        if row==None: return
        self.load_row(row)
        self.errors = FileErrs(self.filename)
            
    def load_row(self, row):
        self.filename    = trim(row[0])
        self.format_code = trim(row[1])
        self.dtd_code    = trim(row[2])
        self.dtd_version = trim(row[3])
        self.calc_filenames()
        self.filesize    = safeint(row[4])
        self.filemode    = safeint(row[5])
        self.modified    = time2str(row[6])
        self.errors.filename = self.filename

    def save(self):
        dict = {'format_code':self.format_code,
                'dtd_code':self.dtd_code,
                'dtd_version':self.dtd_version,
                'filename':self.filename,
                'filesize':999,
                'filemode':self.filemode,
                'modified':self.modified,
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
