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
Lampadas Makefile Module

This module writes out a Makefile for every document in the cache.
"""

# Modules ##################################################################

from DataLayer import lampadas
from Config import config
from Lintadas import lintadas
from Log import log


# Constants


# Globals


class Makefile:

    import os.path
    import urllib
    import os

    def write_all(self):
        log(3, 'Writing Makefile for all documents')
        for dockey in lampadas.Docs.keys():
            self.write_doc(dockey)
        self.write_main_makefile()

    def write_doc(self, DocID):
        log(3, 'Writing Makefile for document ' + str(DocID))
        self.Doc = lampadas.Docs[DocID]
        
        # Determine where files live
        # 
        self.cachedir   = config.cache_dir + str(self.Doc.ID) + '/'
        self.write_makefile(self.Doc, self.cachedir)
        
        log(3, 'Writing Makefile for document ' + str(DocID) + ' complete.')
        

    def write_makefile(self, doc, dir):
        """
        Writes a Makefile to convert the source files into DocBook XML.
        """

        for file in doc.Files.keys():
            File = doc.Files[file]
            if File.is_primary:
                dbsgmlfile = File.basename + '.db.sgml'
                xmlfile = File.basename + '.xml'
                htmlfile = File.basename + '.html'
                indexfile = 'index.html'
                txtfile = File.basename + '.txt'
                omffile = File.basename + '.omf'
                
                Makefile = 'xmlfile = ' + xmlfile + "\n\n"
                if File.FormatID==1 and doc.DTD=='DocBook':
                    Makefile = Makefile + 'BUILD_XML = xmllint --sgml ' + File.file_only + ' > ' + xmlfile + " 2>>xmllint.log; "
                elif File.FormatID==1 and doc.DTD=='LinuxDoc':
                    Makefile = Makefile + 'LD2DBDIR = /usr/local/share/ld2db/' + "\n"
                    Makefile = Makefile + 'BUILD_XML = sgmlnorm -d $(LD2DBDIR)docbook.dcl ' + File.file_only + ' > expanded.sgml 2>>sgmlnorm.log; '
                    Makefile = Makefile + 'jade -t sgml -c $(LD2DBDIR)catalog -d $(LD2DBDIR)ld2db.dsl\\#db expanded.sgml > ' + dbsgmlfile + ' 2>>jade.log; '
                    Makefile = Makefile + 'xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + " 2>>xmllint.log; "
                elif File.FormatID==4 and doc.DTD=='DocBook':
                    pass
                elif File.FormatID==3:
                    Makefile = Makefile + 'BUILD_XML = wt2db -n -s ' + File.file_only + ' -o ' + dbsgmlfile + " 2>>wt2db.log; "
                    Makefile = Makefile + 'xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + " 2>>xmllint.log; "
                elif File.FormatID==6:
                    Makefile = Makefile + 'BUILD_XML = wt2db -n -x ' + File.file_only + ' -o ' + xmlfile + " 2>>wt2db.log; "
                elif File.FormatID==7:
                    Makefile = Makefile + 'BUILD_XML = texi2db -f ' + File.file_only + ' -o ' + xmlfile + " 2>>texi2db.log; "
                else:
                    continue
                Makefile = Makefile + 'tidy -config /etc/lampadas/tidyrc -quiet -f tidy.log -modify ' + xmlfile + "\n"
                
                Makefile = Makefile + "BUILD_HTML = xsltproc --param quiet 1 --maxdepth 100 --nonet --novalid " + config.xslt_html + ' ' + xmlfile + ' > ' + htmlfile + " 2>>xsltproc.log\n"
                Makefile = Makefile + "BUILD_INDEX = xsltproc --param quiet 1 --maxdepth 100 --nonet --novalid " + config.xslt_chunk + ' ' + xmlfile + " 2>>xsltproc.log\n"
                Makefile = Makefile + "BUILD_TXT = lynx --dump --nolist " + htmlfile + ' > ' + txtfile + " 2>>lynx.log\n"
                Makefile = Makefile + "BUILD_OMF = db2omf " + xmlfile + ' -o ' + omffile + " 2>>db2omf.log\n"
                Makefile = Makefile + "\n"

                Makefile = Makefile + "all:\tbuild\n\n"
                
                Makefile = Makefile + "build:\txml html index txt omf\n\n"
                if File.FormatID==4 and doc.DTD=='DocBook':
                    Makefile = Makefile + "xml:\n\n"
                else:
                    Makefile = Makefile + "xml:\t" + xmlfile + "\n\n"
                Makefile = Makefile + "html:\t" + htmlfile + "\n\n"
                Makefile = Makefile + "index:\t" + indexfile + "\n\n"
                Makefile = Makefile + "txt:\t" + txtfile + "\n\n"
                Makefile = Makefile + "omf:\t" + omffile + "\n\n"
                
                Makefile = Makefile + xmlfile + ":\t" + File.file_only + "\n"
                Makefile = Makefile + "\t$(BUILD_XML)\n\n"

                Makefile = Makefile + htmlfile + ":\t" + xmlfile + "\n"
                Makefile = Makefile + "\t$(BUILD_HTML)\n\n"

                Makefile = Makefile + indexfile + ":\t" + xmlfile + "\n"
                Makefile = Makefile + "\t$(BUILD_INDEX)\n\n"

                Makefile = Makefile + txtfile + ":\t" + htmlfile + "\n"
                Makefile = Makefile + "\t$(BUILD_TXT)\n\n"

                Makefile = Makefile + omffile + ":\t" + xmlfile + "\n"
                Makefile = Makefile + "\t$(BUILD_OMF)\n\n"

                Makefile = Makefile + "clean:\n"
                Makefile = Makefile + "\trm -f " + dbsgmlfile + "\n"
                Makefile = Makefile + "\trm -f " + xmlfile + "\n"
                Makefile = Makefile + "\trm -f " + htmlfile + "\n"
                Makefile = Makefile + "\trm -f " + indexfile + "\n"
                Makefile = Makefile + "\trm -f expanded.sgml\n"
                Makefile = Makefile + "\trm -f *.html\n"
                Makefile = Makefile + "\trm -f *.txt\n"
                Makefile = Makefile + "\trm -f *.omf\n"
                Makefile = Makefile + "\trm -f *.log\n"
                Makefile = Makefile + "\n"

                Makefile = Makefile + "rebuild:\tclean build\n\n"
            
                fh = open(dir + 'Makefile', 'w')
                fh.write(Makefile)
                fh.close

    def write_main_makefile(self):
        docsmake = ''
        xmlmake = ''
        htmlmake = ''
        indexmake = ''
        txtmake = ''
        omfmake = ''
        cleanmake = ''
        rebuildmake = ''
        makeneeded = 0
        for docid in lampadas.Docs.keys():
            Doc = lampadas.Docs[docid]
            for file in Doc.Files.keys():
                File = Doc.Files[file]
                if File.is_primary:
                    if (File.FormatID==1 and Doc.DTD=='DocBook') or (File.FormatID==1 and Doc.DTD=='LinuxDoc') or File.FormatID==3 or File.FormatID==6 or File.FormatID==7:
                        makeneeded = 1
                        docsmake = docsmake + "\tcd " + str(docid) + "; $(MAKE) -i all 2>>make.log\n"
                        xmlmake = xmlmake + "\tcd " + str(docid) + "; $(MAKE) -i xml 2>>make.log\n"
                        htmlmake = htmlmake + "\tcd " + str(docid) + "; $(MAKE) -i html 2>>make.log\n"
                        indexmake = indexmake + "\tcd " + str(docid) + "; $(MAKE) -i index 2>>make.log\n"
                        txtmake = txtmake + "\tcd " + str(docid) + "; $(MAKE) -i txt 2>>make.log\n"
                        omfmake = omfmake + "\tcd " + str(docid) + "; $(MAKE) -i omf 2>>db2omf.log\n"
                        cleanmake = cleanmake + "\tcd " + str(docid) + "; $(MAKE) -i clean 2>>make.log\n"
                        rebuildmake = rebuildmake + "\tcd " + str(docid) + "; $(MAKE) -i rebuild 2>>make.log\n"

        if makeneeded:
            Makefile = "all:\tbuild\n\n"
            Makefile = Makefile + "build:\tdocs\n\n"
            Makefile = Makefile + "docs:\n" + docsmake + "\n\n"
            Makefile = Makefile + "xml:\n" + xmlmake + "\n\n"
            Makefile = Makefile + "html:\n" + htmlmake + "\n\n"
            Makefile = Makefile + "index:\n" + indexmake + "\n\n"
            Makefile = Makefile + "txt:\n" + txtmake + "\n\n"
            Makefile = Makefile + "omf:\n" + omfmake + "\n\n"
            Makefile = Makefile + "clean:\n" + cleanmake + "\n\n"
            Makefile = Makefile + "rebuild:\n" + rebuildmake + "\n\n"

            fh = open(config.cache_dir + 'Makefile', 'w')
            fh.write(Makefile)
            fh.close


makefile = Makefile()


if __name__=="__main__":
#	makefile.write_main_makefile()
    makefile.write_all()

