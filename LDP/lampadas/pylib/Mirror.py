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
from Log import log
from Config import config

# Constants


# Globals


class Mirror:

    import os.path
    import urllib
    import os

    def mirror_all(self):
        log(3, 'Mirroring all documents')
        for dockey in lampadas.Docs.keys():
            self.mirror_doc(dockey)

    def mirror_doc(self, DocID):
        log(3, 'Mirroring document ' + str(DocID))
        self.Doc = lampadas.Docs[DocID]
        
        # decide if the document is remote
        #
        self.is_remote = 0
        filekeys = self.Doc.Files.keys()
        for filekey in filekeys:
            if not self.Doc.Files[filekey].IsLocal:
                self.is_remote = 1
        
        # delete list of local files if document is remote
        #
        if self.is_remote:
                filekeys = self.Doc.Files.keys()
                for filekey in filekeys:
                    if self.Doc.Files[filekey].IsLocal:
                        self.Doc.Files[filekey].Del()

        # mirror all files into cache, whether from remote
        # or local storage
        #
        # filename can look like:	http://foo.org/foo.sgml
        # 							ftp://foo.org/foo.sgml
        # 							howto/docbook/big-memory-howto.sgml
        # 
        for filekey in filekeys:
            
            # create cache directory for this document
            # 
            self.cachedir = config.cache_dir + str(self.Doc.ID) + '/'
            if not self.os.access(self.cachedir, self.os.F_OK):
                self.os.mkdir(self.cachedir)

            self.File		= self.Doc.Files[filekey]
            self.filename	= self.File.Filename
            self.file_only	= self.File.file_only
            self.cachename	= self.cachedir + self.file_only
            
            if self.File.IsLocal:

                # It is expensive to copy local documents into a cache directory,
                # but it avoids publishing documents directly out of CVS.
                # Some publishing tools leave clutter in the directory on failure.
                # 
                if not self.os.access(config.cvs_root + self.filename, self.os.F_OK):
                    log(2, 'Cannot mirror missing file: ' + self.filename)
                    continue
                log(3, 'mirroring local file ' + self.filename)
                command = 'cd ' + self.cachedir + '; cp -pu ' + config.cvs_root + self.filename + ' .'
                self.os.system(command)
        
            else:
                try:
                    log(3, 'mirroring remote file ' + self.filename)
                    self.urllib.urlretrieve(self.File.Filename, self.cachename)
                except IOError:
                    log(0, 'error retrieving remote file ' + self.filename)
                    continue

            if self.unpack(self.cachedir, self.file_only):
                for file in self.os.listdir(self.cachedir):
                    if file[-5:] <> '.html':
                        self.Doc.Files.Add(self.Doc.ID, file)

        log(3, 'Mirroring document ' + str(DocID) + ' complete.')
        

    def unpack(self, dir, file):
        """
        Goes to the specified directory and unpacks a file.
        Returns 1 if an archive was identified and unpacked.
        Returns 0 if it was not a recognized archive.
        Supported archives are .tar, .gz and .tar.gz.
        """
        cmd_start = 'cd ' + dir + '; '
        if file[-7:] == '.tar.gz':
            self.os.system(cmd_start + 'tar -zxf ' + file)
            return 1
        elif file[-4:] == '.tar':
            self.os.system(cmd_start + 'tar -xf ' + file)
            return 1
        elif file[-3:] == '.gz':
            self.os.system(cmd_start + 'gunzip -f ' + file)
            return 1


if __name__ == "__main__":
    M = Mirror()
    M.mirror_all()

