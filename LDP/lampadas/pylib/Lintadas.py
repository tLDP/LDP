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


# Constants


# Globals

ERR_FILE_NOT_FOUND = 1
ERR_FILE_NOT_WRITABLE = 2
ERR_NO_SOURCE_FILE = 3
ERR_NO_PRIMARY_FILE = 4
ERR_TWO_PRIMARY_FILES = 5


# Lintadas

class Lintadas:

    def check_all(self):
        keys = lampadas.docs.keys()
        for key in keys:
            self.check(key)
    
    def check(self, doc_id):
        log(3, 'Running Lintadas on document ' + str(doc_id))
        doc = lampadas.docs[doc_id]
        assert not doc==None
        doc.errors.clear()

        self.check_files(doc_id)
        self.check_maintained(doc_id)

        doc.save()
        log(3, 'Lintadas run on document ' + str(doc_id) + ' complete')

    def check_files(self, doc_id):
        doc = lampadas.docs[doc_id]

        if doc.files.count()==0:
            self.add_error(doc_id, ERR_NO_SOURCE_FILE)
            return

        top = 0

        keys = doc.files.keys()
        for key in keys:
            file = doc.files[key]

            if file.top > 0:
                top = top + 1

            if file.local==0:
                log(3, 'Skipping remote file ' + key)
                continue
                
            log(3, 'Checking filename ' + key)
            if not os.access(config.cvs_root + file.filename, os.F_OK):
                self.add_error(doc_id, ERR_FILE_NOT_FOUND)

            # Determine file format
            self.filename = file.filename.upper()
            if self.filename[-5:]=='.SGML':
                FileFormat = "SGML"
                DocFormat = 'SGML'
            elif self.filename[-4:]=='.XML':
                FileFormat = "XML"
                DocFormat = 'XML'
            elif self.filename[-3:]=='.WT':
                FileFormat = 'WIKI'
                DocFormat = 'WIKI'
            else:
                FileFormat = ''
                DocFormat = ''

            formatkeys = lampadas.formats.keys()
            for formatkey in formatkeys:
                if lampadas.formats[formatkey].name['EN']==FileFormat:
                    file.Formatid = formatkey
                if lampadas.formats[formatkey].name['EN']==DocFormat:
                    doc.Formatid = formatkey
            
            log(3, 'file format is ' + FileFormat)
            
            # Determine DTD for SGML and XML files
            if FileFormat=='XML' or FileFormat=='SGML':
                dtd_version = ''
                try:
                    command = 'grep -i DOCTYPE ' + config.cvs_root + file.filename + ' | head -n 1'
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

            log(3, 'doc dtd is ' + doc.dtd_code)

            file.save()

        if top==0:
            self.add_error(doc_id, ERR_NO_PRIMARY_FILE)

        if top > 1:
            self.add_error(doc_id, ERR_TWO_PRIMARY_FILES)

    def check_maintained(self, doc_id):
        doc = lampadas.docs[doc_id]
        maintained = 0
        keys = doc.users.keys()
        for key in keys:
            docuser = doc.users[key]
            if docuser.active==1 and docuser.role_code=='author' or docuser.role_code=='maintainer':
                maintained = 1
        doc.maintained = maintained

    def add_error(self, doc_id, err_id):
        log(2, 'Error: ' + str(err_id))
        doc = lampadas.docs[doc_id]
        doc.errors.add(err_id)


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
        print "Running on all documents..."
        lintadas.check_all()
    else:
        for doc_id in docs:
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
