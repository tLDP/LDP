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
"""
Lampadas Error Checking Module

This module performs all kinds of automatic checks on the Lampadas
system. It checks for erroroneous data in the database, 
and the source files it points to. Errors are logged in the
document_error and file_error table, according to which object
the error is attributed.

This module works closely with the 
"""

# Modules ##################################################################

from Globals import *
from Config import config
from Log import log
import os
import stat
import string
import time

from CoreDM import dms

class Lintadas:
    """
    Updates file and document meta-data and analyzes  it for errors.

    NOTE: You must always check files *before* checking documents,
    so that the file meta-data is up to date. Checking the documents
    will pull the top file's meta-data over into the document,
    if there is no conflicting value already set for the document.
    """

    # FIXME: These should be loaded from a configuration file so they
    # are easily configurable by the administrator.
    def update_metadata(self):
        docs = dms.document.get_all()
        for key in docs.keys():
            doc = docs[key]
            doc.update_metadata()

    def check_files(self, doc_id=None):
        """Checks files for errors. Checks all files by default, but you can
        also check the files belonging to a single document."""

        # Decide which files to check for errors.
        if doc_id==None:
            sourcefiles = dms.sourcefile.get_all()
            keys = sourcefiles.keys('filename')
        else:
            doc = dms.document.get_by_id(doc_id)
            keys = doc.files.keys('filename')
            
        # Check the files for errors.
        for key in keys:
            self.check_file(key)
            
    def check_docs(self):
        # Preload data if we're checking all files.
        docusers = dms.document_user.get_all()
        docfiles = dms.document_file.get_all()
        sourcefiles = dms.sourcefile.get_all()
        docs = dms.document.get_all()
        for key in docs.keys():
            self.check_doc(key)
    
    def check_file(self, filename):
        log(3, 'Running Lintadas on file ' + filename)
        sourcefile = dms.sourcefile.get_by_id(filename)

        sourcefile.read_metadata()

        # CLear out errors before checking
        sourcefile.errors.clear()

        # Do not check remote files.
        # FIXME: It should check the local file if it has been
        # downloaded already.
        if sourcefile.local==0:
            log(3, 'Skipping remote file ' + filename)
            return
        
        filename = sourcefile.localname
        
        # If file the is missing, flag error and stop.
        if os.access(filename, os.F_OK)==0:
            err = dms.file_error.new()
            err.err_id = ERR_FILE_NOT_FOUND
            err.filename = sourcefile.filename
            sourcefile.errors.add(err)
            return

        # If file is not readable, flag error and top.
        if os.access(filename, os.R_OK)==0:
            err = dms.file_error.new()
            err.err_id = ERR_FILE_NOT_READABLE
            err.filename = sourcefile.filename
            sourcefile.errors.add(err)
            return

        # Read file information
        filestat = os.stat(filename)
        sourcefile.filesize = filestat[stat.ST_SIZE]
        sourcefile.filemode = filestat[stat.ST_MODE]
        sourcefile.modified = time.ctime(filestat[stat.ST_MTIME])
        
        sourcefile.read_metadata()
        if stat.S_ISDIR(sourcefile.filemode)==1:
            sourcefile.format_code = 'dir'

        # If we were able to read format code, post it to the document,
        if sourcefile.format_code=='':
            err = dms.file_error.new()
            err.err_id = ERR_FILE_FORMAT_UNKNOWN
            err.filename = sourcefile.filename
            sourcefile.errors.add(err)

    def check_doc(self, doc_id):
        """
        Check for errors at the document level.
        """

        log(3, 'Running Lintadas on document ' + str(doc_id))
        doc = dms.document.get_by_id(doc_id)
       
        # See if the document is maintained
        maintained = 0
        for key in doc.users.keys():
            docuser = doc.users[key]
            if docuser.active==1 and (docuser.role_code=='author' or docuser.role_code=='maintainer'):
                maintained = 1
        doc.maintained = maintained

        # Clear any existing errors
        doc.errors.delete_by_keys([['err_type_code', '=', 'doc']])

        # If document is not active or archived, do not flag
        # any errors against it.
        if doc.pub_status_code<>'N':
            return

        # Flag an error against the *doc* if there are no files.
        if doc.files.count()==0:
            err = doc.errors.new()
            err.doc_id = doc.id
            err.err_id = ERR_NO_SOURCE_FILE
            err.notes = ''
            doc.errors.add(err)
        else:

            # Count the number of top files. There muse be exactly one.
            # This takes advantage of the fact that true=1 and false=0.
            top = 0
            for key in doc.files.keys():
                if doc.files[key].top:
                    top = top + 1
            if top==0:
                err = doc.errors.new()
                err.doc_id = doc.id
                err.err_id = ERR_NO_PRIMARY_FILE
                err.notes = ''
                doc.errors.add(err)
            if top > 1:
                err = doc.errors.new()
                err.doc_id = doc.id
                err.err_id = ERR_TWO_PRIMARY_FILES
                err.notes = ''
                doc.errors.add(err)

        doc.lint_time = now_string()
        log(3, 'Lintadas run on document ' + str(doc_id) + ' complete')


lintadas = Lintadas()

# When run at the command line, check the document requested.
# If no document was specified, all checks are performed on all documents.
# 

def main():
    import getopt
    import sys

    config.logcon = 1
    config.log_level = 3
    doc_ids = sys.argv[1:]
    if len(doc_ids)==0:

        # Prefetch data to make things run faster...
        print 'Prefetching data for faster performance...'
        print '  Fetching documents...'
        docs = dms.document.get_all()
        print '  Fetching source files...'
        sourcefiles = dms.sourcefile.get_all()
        print '  Fetching document files...'
        docfiles = dms.document_file.get_all()

        print 'Checking all source files for errors...'
        for key in sourcefiles.keys():
            sourcefile = sourcefiles[key]
            print '  Checking file ' + sourcefile.filename
            lintadas.check_file(sourcefile.filename)
            sourcefile.save()

        print 'Updating document metadata and error checking...'
        for key in docs.keys():
            doc = docs[key]
            print '  Checking and updating metadata in document ' + str(doc.id) + ' ' + doc.title
            doc.update_metadata()
            lintadas.check_doc(doc.id)
            doc.save()
    else:
        for doc_id in doc_ids:
            print '  Checking document ' + str(doc_id) + ' for errors...'
            doc = dms.document.get_by_id(int(doc_id))
            lintadas.check_doc(int(doc_id))
            doc.save()
    print 'Done.'

def usage():
    print "Lintadas version " + VERSION
    print
    print "This is part of the Lampadas System"
    print
    print "Pass doc ids to run Lintadas on specific docs,"
    print "or call with no parameters to run Lintadas on all docs."
    print


if __name__=="__main__":
    main()
