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
from DataLayer import lampadas
from SourceFiles import sourcefiles
import os
import stat
import string
import time


# Lintadas

class Lintadas:
    """
    Updates file and document meta-data and analyzes  it for errors.

    NOTE: You must always check files *before* checking documents,
    so that the file meta-data is up to date. Checking the documents
    will pull the top file's meta-data over into the document.

    Alternatively, you can call import_docs_metadata() at any time
    to only upload meta-data from files to documents.
    """

    # FIXME: These should be loaded from a configuration file so they
    # are easily configurable by the administrator.

    # This is a list of file extensions and the file types
    # they represent.
    extensions = {
        'sgml': 'sgml',
        'xml':  'xml',
        'wt':   'wikitext',
        'txt':  'text',
        'texi': 'texinfo',
        'sh':   'shell',
    }

    def check_files(self):
        keys = sourcefiles.keys()
        for key in keys:
            self.check_file(key)
            
    def check_docs(self):
        keys = lampadas.docs.keys()
        for key in keys:
            self.check_doc(key)
    
    def check_file(self, filename):
        log(3, 'Running Lintadas on file ' + filename)
        sourcefile = sourcefiles[filename]

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
            sourcefile.errors.add(ERR_FILE_NOT_FOUND)
            return

        # If file is not readable, flag error and top.
        if os.access(filename, os.R_OK)==0:
            sourcefile.errors.add(ERR_FILE_NOT_READABLE)
            return

        # Read file information
        filestat = os.stat(filename)
        sourcefile.filesize = filestat[stat.ST_SIZE]
        sourcefile.filemode = filestat[stat.ST_MODE]
        sourcefile.modified = time.ctime(filestat[stat.ST_MTIME])

        # Determine file format.
        file_extension = string.lower(string.split(filename, '.')[-1])
        if self.extensions.has_key(file_extension) > 0:
            sourcefile.format_code = self.extensions[file_extension]
        
        # If we were able to read format code, post it to the document,
        if sourcefile.format_code=='':
            sourcefile.errors.add(ERR_NO_FORMAT_CODE)

        # Determine DTD for SGML and XML files
        if sourcefile.format_code=='xml' or sourcefile.format_code=='sgml':
            sourcefile.dtd_code, sourcefile.dtd_version = self.read_file_dtd(filename)
        else:
            sourcefile.dtd_code = 'N/A'
            sourcefile.dtd_version = ''
        
        sourcefile.save()

    def read_file_dtd(self, filename):
        """
        Determines a file's DTD and DTD version if possible.
        Returns a tuple, (DTD, VERSION).
        """

        dtd_code, dtd_version = '', ''
        try:
            fh = open(filename, 'r', 1)
            while (1):
                line = fh.readline()
                if line=='':
                    break
                line = line.upper()
                pos = line.find('DOCTYPE')
                if pos > 0:
                    pos = line.find('DOCBOOK')
                    if pos > 0:
                        dtd_code = 'DocBook'
                        line = trim(line[pos + 7:])
                        if line[:3]=='XML':
                            line = trim(line[3:])
                        if line[0]=='V':
                            line = line[1:]
                            pos = line.find('//')
                            if pos > 0:
                                dtd_version = line[:pos]
                                break
                    else:
                        pos = line.find('LINUXDOC')
                        if pos > 0:
                            dtd_code = 'LinuxDoc'
                            line = trim(line[pos + 8:])
                        else:
                            continue
            fh.close()

        except IOError:
            pass
            
        return dtd_code, dtd_version

    def check_doc(self, doc_id):
        """
        Check for errors at the document level.
        """

        log(3, 'Running Lintadas on document ' + str(doc_id))
        doc = lampadas.docs[doc_id]
        filenames = doc.files.keys()
        usernames = doc.users.keys()
       
        # See if the document is maintained
        maintained = 0
        for username in usernames:
            docuser = doc.users[username]
            if docuser.active==1 and (docuser.role_code=='author' or docuser.role_code=='maintainer'):
                maintained = 1
        doc.maintained = maintained

        # Clear any existing errors
        doc.errors.clear()

        # If document is not active or archived, do not flag
        # any errors against it.
        if doc.pub_status_code<>'N' and doc.pub_status_code<>'A':
            return

        # Flag an error against the *doc* if there are no files.
        if doc.files.count()==0:
            doc.errors.add(ERR_NO_SOURCE_FILE)
        else:

            # Count the number of top files. There muse be exactly one.
            # This takes advantage of the fact that true=1 and false=0.
            top = 0
            for filename in filenames:
                if doc.files[filename].top:
                    top = top + 1
            if top==0:
                doc.errors.add(ERR_NO_PRIMARY_FILE)
            if top > 1:
                doc.errors.add(ERR_TWO_PRIMARY_FILES)

        doc.save()
        log(3, 'Lintadas run on document ' + str(doc_id) + ' complete')

    def import_docs_metadata(self):
        doc_ids = lampadas.docs.keys()
        for doc_id in doc_ids:
            self.import_doc_metadata(doc_id)

    def import_doc_metadata(self, doc_id):
        doc = lampadas.docs[doc_id]
        filenames = doc.files.keys()
        for filename in filenames:
            docfile = doc.files[filename]
            if docfile.top==1:
                sourcefile      = sourcefiles[filename]
                doc.format_code = sourcefile.format_code
                doc.dtd_code    = sourcefile.dtd_code
                doc.dtd_version = sourcefile.dtd_version
                doc.save()


lintadas = Lintadas()

# When run at the command line, check the document requested.
# If no document was specified, all checks are performed on all documents.
# 

def main():
    import getopt
    import sys

    config.logcon = 1
    config.log_level = 3
    docs = sys.argv[1:]
    if len(docs)==0:
        print 'Checking all documents for errors...'
        lintadas.check_docs()
        print 'Checking all source files for errors...'
        lintadas.check_files()
        print 'Updating Meta-data on all documents...'
        lintadas.import_docs_metadata()
    else:
        for doc_id in docs:
            print 'Checking document ' + str(doc_id) + ' for errors...'
            lintadas.check_doc(int(doc_id))
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
