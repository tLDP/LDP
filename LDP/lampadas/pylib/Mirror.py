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

from DataLayer import lampadas
from SourceFiles import sourcefiles
from Log import log
from Config import config
import urllib
import os


# Constants


# Globals


class Mirror:

    def mirror_all(self):
        log(3, 'Mirroring all documents')
        for dockey in lampadas.docs.keys():
            self.mirror(dockey)

    def mirror(self, doc_id):
        log(3, 'Mirroring document ' + str(doc_id))
        doc = lampadas.docs[doc_id]
        
        # decide if the document is remote
        docremote = 0
        filekeys = doc.files.keys()
        for filekey in filekeys:
            if sourcefiles[filekey].local==0:
                docremote = 1
        
        # If document has a single remote file,
        # delete list of local files.
        if docremote==1:
            filekeys = doc.files.keys()
            for filekey in filekeys:
                if sourcefiles[filekey].local==1:
                    doc.files[filekey].delete()

        # mirror all files into cache, whether from remote
        # or local storage
        #
        # filename can look like:
        #   http://foo.org/foo.sgml             Pull via HTTP
        #   ftp://foo.org/foo.sgml              Pull via FTP
        #   file://foo.org/foo.sgml             Local, but outside CVS
        #   howto/docbook/big-memory-howto.sgml In CVS tree
        # 
        for filekey in filekeys:
            
            # create cache directory for this document
            cachedir = config.cache_dir + str(doc.id) + '/'
            if not os.access(cachedir, os.F_OK):
                os.mkdir(cachedir)
            workdir = cachedir + 'work/'
            if not os.access(workdir, os.F_OK):
                os.mkdir(workdir)
            logdir = workdir + 'log/'
            if not os.access(logdir, os.F_OK):
                os.mkdir(logdir)

            docfile     = doc.files[filekey]
            sourcefile  = sourcefiles[filekey]
            filename    = sourcefile.localname
            file_only   = sourcefile.file_only
            workname    = workdir + file_only
            
            if sourcefile.local==1:

                # It is expensive to copy local documents into a cache directory,
                # but it avoids publishing documents directly out of CVS.
                # Some publishing tools leave clutter in the directory on failure.
                if not os.access(filename, os.F_OK):
                    log(2, 'Cannot mirror missing file: ' + filename)
                    continue
                log(3, 'mirroring local file ' + filename)
                command = 'cd ' + workdir + '; cp -pu ' + filename + ' .'
                os.system(command)
        
            else:
                try:
                    log(3, 'mirroring remote file ' + filename)
                    urllib.urlretrieve(sourcefile.filename, workname)
                except IOError:
                    log(0, 'error retrieving remote file ' + filename)
                    continue

            if self.unpack(workdir, file_only):
                for file in os.listdir(workdir):
                    if file[-5:] <> '.html':
                        doc.files.add(doc.id, file)

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

