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

This module performs all kinds of automatic checks on data in the database
and the source files it points to. Errors are logged in the
document_error table.
"""

# Modules ##################################################################

from Globals import *
from Config import config
from Log import log
from DataLayer import lampadas
import os
import stat
import string
import time


# Constants


# Globals

ERR_NO_SOURCE_FILE = 3
ERR_NO_PRIMARY_FILE = 4
ERR_TWO_PRIMARY_FILES = 5
ERR_NO_FORMAT_CODE = 7

ERR_FILE_NOT_FOUND = 1
ERR_FILE_NOT_WRITABLE = 2
ERR_FILE_NOT_READABLE = 6

# Lintadas

class Lintadas:

    # This is a list of file extensions and the file types
    # they represent.
    extensions = {
        'sgml': 'sgml',
        'xml':  'xml',
        'wt':   'wikitext',
        'txt':  'text',
        'texi': 'texinfo',
    }

    def check_all(self):
        keys = lampadas.docs.keys()
        for key in keys:
            self.check(key)
    
    def check(self, doc_id):
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
        for filename in filenames:
            file = doc.files[filename]
            file.errors.clear()

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
                top = top + doc.files[filename].top
            if top==0:
                doc.errors.add(ERR_NO_PRIMARY_FILE)
            if top > 1:
                doc.errors.add(ERR_TWO_PRIMARY_FILES)

            for filename in filenames:
                file = doc.files[filename]
                file.errors.clear()

                # Do not check remote files.
                # FIXME: It should check the local file if it has been
                # downloaded already.
                if file.local==0:
                    log(3, 'Skipping remote file ' + filename)
                    continue
                
                log(3, 'Checking filename ' + filename)
                if file.in_cvs==1:
                    filename = file.cvsname
                else:
                    filename = file.localname
                
                # If file the is missing, flag error and stop.
                if os.access(filename, os.F_OK)==0:
                    file.errors.add(ERR_FILE_NOT_FOUND)
                    continue

                # If file is not readable, flag error and top.
                if os.access(filename, os.R_OK)==0:
                    file.errors.add(ERR_FILE_NOT_READABLE)
                    continue

                # Read file information
                filestat = os.stat(filename)
                file.filesize = filestat[stat.ST_SIZE]
                file.filemode = filestat[stat.ST_MODE]
                file.modified = time.ctime(filestat[stat.ST_MTIME])

                # Determine file format.
                file_extension = string.lower(string.split(filename, '.')[-1])
                if self.extensions.has_key(file_extension) > 0:
                    file.format_code = self.extensions[file_extension]
                
                # If we were able to read format code, post it to the document,
                if file.format_code=='':
                    file.errors.add(ERR_NO_FORMAT_CODE)

                # Determine DTD for SGML and XML files
                if file.format_code=='xml' or file.format_code=='sgml':
                    file.dtd_code, file.dtd_version = self.read_file_dtd(filename)
                else:
                    file.dtd_code = 'N/A'
                    file.dtd_version = ''
                
                # If this was the top file, post to document.
                if file.top==1:
                    doc.format_code = file.format_code
                    doc.dtd_code = file.dtd_code
                    doc.dtd_version = file.dtd_version

                # FIXME: need a way to keep track of who is managing these fields.
                # Probably it should be managed by Lampadas, but allow the user
                # the ability to override it with their setting.
                
                file.save()

        doc.save()
        log(3, 'Lintadas run on document ' + str(doc_id) + ' complete')

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
        print "Running Lintadas on all documents..."
        lintadas.check_all()
    else:
        for doc_id in docs:
            print "Running Lintadas on document " + str(doc_id)
            lintadas.check(int(doc_id))

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
