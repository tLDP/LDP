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

from Config import config
from Log import log
from DataLayer import lampadas
import os
import string


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
            if docuser.active==1 and docuser.role_code=='author' or docuser.role_code=='maintainer':
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

        if doc.format_code=='':
            doc.errors.add(ERR_NO_FORMAT_CODE)

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
                if file.local==0:
                    log(3, 'Skipping remote file ' + filename)
                    continue
                
                log(3, 'Checking filename ' + filename)
                filename = config.cvs_root + file.filename
                
                # If file the is missing, flag error and stop.
                if os.access(filename, os.F_OK)==0:
                    file.errors.add(ERR_FILE_NOT_FOUND)
                    continue

                # If file is not readable, flag error and top.
                if os.access(filename, os.R_OK)==0:
                    file.errors.add(ERR_FILE_NOT_READABLE)
                    continue

                # Determine file format.
                file_extension = string.lower(string.split(filename, '.')[-1])
                if self.extensions.has_key(file_extension) > 0:
                    file.format_code = self.extensions[file_extension]
                
                # Determine DTD for SGML and XML files
                if file.format_code=='xml' or file.format_code=='sgml':
                    file.dtd = self.read_file_dtd(filename)


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
        
        dtd_code = ''
        fh = open(filename, 'r', 1)
        line = fh.readline()
        while line:
            line = line.upper()
            pos = line.find('DOCTYPE')
            if pos > 0:
                if line.count('DOCBOOK') > 0:
                    dtd_code = 'DocBook'
                elif line.count('LINUXDOC') > 0:
                    dtd_code = 'LinuxDoc'
                break
            line = fh.readline()
        fh.close()
        return dtd_code

        dtd_version = ''
        try:
            command = 'grep -i DOCTYPE ' + filename + ' | head -n 1'
            grep = os.popen(command, 'r')
            dtd_version = grep.read()
        except IOError:
            pass

        dtd_version = dtd_version.upper()
        if dtd_version.count('DOCBOOK') > 0:
            doc.dtd_code = 'DocBook'
        elif dtd_version.count('LINUXDOC') > 0:
            doc.dtd_code = 'LinuxDoc'
        else:
            doc.dtd_code = ''


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
