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
Lampadas Mirroring Module

This module mirrors documents whose source files are located outside the
local Lampdas system.
"""

# Modules ##################################################################

from Globals import *
from Log import log
from Config import config
import urllib
import os

from CoreDM import dms

class Mirror:

    def mirror_all(self):
        log(3, 'Mirroring all documents')
        docs = dms.document.get_all()
        for dockey in docs.sort_by('id'):
            self.mirror(dockey)

    def mirror(self, doc_id):
        log(3, 'Mirroring document ' + str(doc_id))
        doc = dms.document.get_by_id(doc_id)

        if doc.lint_time=='':
            return

        # Create cache directories for this document,
        # even if we do nothing else.
        cachedir = config.cache_dir + str(doc.id) + '/'
        if not os.access(cachedir, os.F_OK):
            os.mkdir(cachedir)
        workdir = cachedir + 'work/'
        if not os.access(workdir, os.F_OK):
            os.mkdir(workdir)
        logdir = workdir + 'log/'
        if not os.access(logdir, os.F_OK):
            os.mkdir(logdir)

        # Do not attempt to mirror a document which has document or file errors.
        if doc.errors.count([['err_type_code', '=', 'doc']]) > 0 or doc.file_error_count > 0:
            print 'Not mirroring document ' + str(doc.id) + '; it has errors.'
            return

        # Clear mirroring errors before adding new ones.
        doc.errors.delete_by_keys([['err_type_code', '=', 'mirror']])
        
        # Decide if the document is remote or local
        docremote = 0
        for key in doc.files.keys():
            if doc.files[key].sourcefile.local==0:
                docremote = 1
        
        # FIXME: Actually use a field to indicate that these records are
        # transient. Then we can use the simpler and faster .clear() method.
        
        # If document has a single remote file,
        # delete list of local files.
        if docremote==1:
            doc.files.delete_by_keys([['local', '=', 1]])

        # mirror all files into cache, whether from remote
        # or local storage
        #
        # filename can look like:
        #   http://foo.org/foo.sgml             Pull via HTTP
        #   ftp://foo.org/foo.sgml              Pull via FTP
        #   file://foo.org/foo.sgml             Local, but outside CVS
        #   howto/docbook/big-memory-howto.sgml In CVS tree
        # 
        for key in doc.files.keys():
            docfile     = doc.files[key]
            sourcefile  = docfile.sourcefile
            filename    = sourcefile.localname
            file_only   = sourcefile.file_only
            workname    = workdir + file_only
            
            if sourcefile.local==1:

                # It is expensive to copy local documents into a cache directory,
                # but it avoids publishing documents directly out of CVS.
                # Some publishing tools leave clutter in the directory on failure.
                if not os.access(filename, os.F_OK):
                    log(2, 'Cannot mirror missing file: ' + filename)
                    err = dms.file_error.new()
                    err.err_id = ERR_MIRROR_NOT_FOUND
                    err.filename = docfile.filename
                    docfile.sourcefile.errors.add(err)
                    continue

                if sourcefile.format_code=='dir':
                    log(3, 'mirroring local directory ' + filename)
                    command = 'cd ' + workdir + '; cp -upr ' + filename + ' .'
                else:
                    log(3, 'mirroring local file ' + filename)
                    command = 'cd ' + workdir + '; cp -up ' + filename + ' .'
                print command
                os.system(command)
        
            else:
                try:
                    log(3, 'mirroring remote file ' + filename)
                    urllib.urlretrieve(sourcefile.filename, workname)
                except IOError:
                    log(0, 'error retrieving remote file ' + filename)
                    err = dms.file_error.new()
                    err.err_id = ERR_MIRROR_URL_RETRIEVE
                    err.filename = docfile.filename
                    docfile.sourcefile.errors.add(err)
                    continue

            if self.unpack(workdir, file_only):
                for file in os.listdir(workdir):
                    if file[-5:] <> '.html':
                        doc.files.add(doc.id, file)

        if doc.errors.count([['err_type_code', '=', 'mirror']])==0 and doc.file_error_count==0:
            doc.mirror_time = now_string()
        doc.files.save()
        doc.save()
        log(3, 'Mirroring document ' + str(doc_id) + ' complete.')

    def unpack(self, dir, file):
        """
        Goes to the specified directory and unpacks a file.
        Returns 1 if an archive was identified and unpacked.
        Returns 0 if it was not a recognized archive.
        Supported archives are .tar, .gz and .tar.gz.
        """
        cmd_start = 'cd ' + dir + '; '
        if file[-7:]=='.tar.gz':
            os.system(cmd_start + 'tar -zxf ' + file)
            return 1
        elif file[-4:]=='.tar':
            os.system(cmd_start + 'tar -xf ' + file)
            return 1
        elif file[-3:]=='.gz':
            os.system(cmd_start + 'gunzip -f ' + file)
            return 1

mirror = Mirror()

if __name__=="__main__":
    print "Running Mirror on all documents..."
    mirror.mirror_all()

