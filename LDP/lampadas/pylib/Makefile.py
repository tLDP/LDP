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

XSLTPROC_PARAMS = ''


# Globals


class Makefile:

    def write_all(self):
        log(3, 'Writing Makefile for all documents')
        for dockey in lampadas.docs.keys():
            self.write(dockey)
        self.write_main_makefile()

    def write(self, doc_id):
        log(3, 'Writing Makefile for document ' + str(doc_id))
        doc = lampadas.docs[doc_id]
        
        # Determine where files live
        cachedir   = config.cache_dir + str(doc.id) + '/'
        self.write_makefile(doc, cachedir)
        
        log(3, 'Writing Makefile for document ' + str(doc_id) + ' complete.')
        

    def write_makefile(self, doc, dir):
        """
        Writes a Makefile to convert the source files into DocBook XML.
        """

        if doc.errors.count() > 0 or (doc.pub_status_code<>'A' and doc.pub_status_code<>'N'):
            return

        for file in doc.files.keys():
            file = doc.files[file]
            if file.top==1 and file.errors.count()==0:
                
                log(3, 'Found top file: ' + file.filename)
                dbsgmlfile = file.basename + '.db.sgml'
                xmlfile = file.basename + '.xml'
                htmlfile = file.basename + '.html'
                indexfile = 'index.html'
                txtfile = file.basename + '.txt'
                omffile = file.basename + '.omf'
                
                Makefile = 'xmlfile = ' + xmlfile + "\n\n"

                # DocBook SGML
                if file.format_code=='sgml' and doc.dtd_code=='DocBook':
                    Makefile = Makefile + 'BUILD_XML = xmllint --sgml ' + file.file_only + ' > ' + xmlfile + " 2>>xmllint.log; "


                # LinuxDoc SGML
                elif file.format_code=='sgml' and doc.dtd_code=='LinuxDoc':
                    Makefile = Makefile + 'LD2DBDIR = /usr/local/share/ld2db/\n'
                    Makefile = Makefile + 'BUILD_DOCBOOK = sgmlnorm -d $(LD2DBDIR)docbook.dcl ' + file.file_only + ' > expanded.sgml 2>>sgmlnorm.log; '
                    Makefile = Makefile + 'jade -t sgml -c $(LD2DBDIR)catalog -d $(LD2DBDIR)ld2db.dsl\\#db expanded.sgml > ' + dbsgmlfile + ' 2>>jade.log\n'
                    Makefile = Makefile + 'BUILD_XML = xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + " 2>>xmllint.log; "

                # DocBook XML
                elif file.format_code=='xml' and doc.dtd_code=='DocBook':
                    Makefile = Makefile + 'BUILD_XML = '

                # WikiText
                elif file.format_code=='wikitext':
                    Makefile = Makefile + 'BUILD_XML = wt2db -n -s ' + file.file_only + ' -o ' + dbsgmlfile + " 2>>wt2db.log; "
                    Makefile = Makefile + 'xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + " 2>>xmllint.log; "

                # Text
                elif file.format_code=='text':
                    Makefile = Makefile + 'BUILD_XML = wt2db -n -x ' + file.file_only + ' -o ' + xmlfile + " 2>>wt2db.log; "

                # Texinfo
                elif file.format_code=='texinfo':
                    Makefile = Makefile + 'BUILD_XML = texi2db -f ' + file.file_only + ' -o ' + xmlfile + " 2>>texi2db.log; "

                # Unrecognized
                else:
                    # Complain loudly if we can't handle the format.
                    # Theoretically shouldn't happen, or the doc would have had errors.
                    print 'ERROR in document ' + str(doc.id) + ': format_code ' + file.format_code
                    log(3, 'unrecognized format code: ' + file.format_code)
                    continue
                    
                Makefile = Makefile + 'tidy -config /etc/lampadas/tidyrc -quiet -f tidy.log -modify ' + xmlfile + "\n"
                
                Makefile = Makefile + "BUILD_HTML = xsltproc --param quiet 1 --maxdepth 100 " + XSLTPROC_PARAMS + ' ' + config.xslt_html + ' ' + xmlfile + ' > ' + htmlfile + " 2>>xsltproc.log\n"
                Makefile = Makefile + "BUILD_INDEX = xsltproc --param quiet 1 --maxdepth 100 " + XSLTPROC_PARAMS + ' ' + config.xslt_chunk + ' ' + xmlfile + " 2>>xsltproc.log\n"
                Makefile = Makefile + "BUILD_TXT = lynx --dump --nolist " + htmlfile + ' > ' + txtfile + " 2>>lynx.log\n"
                Makefile = Makefile + "BUILD_OMF = db2omf " + xmlfile + ' -o ' + omffile + " 2>>db2omf.log\n"
                Makefile = Makefile + "\n"

                Makefile = Makefile + "all:\tbuild\n\n"
                
                Makefile = Makefile + "build:\tdocbook xml html index txt omf\n\n"

                if file.format_code=='sgml' and doc.dtd_code=='LinuxDoc':
                    Makefile = Makefile + 'docbook:\t' + dbsgmlfile + '\n\n'
                else:
                    Makefile = Makefile + "docbook:\n\n"

                if file.format_code=='xml' and doc.dtd_code=='DocBook':
                    Makefile = Makefile + "xml:\n\n"
                else:
                    Makefile = Makefile + "xml:\t" + xmlfile + "\n\n"

                Makefile = Makefile + "html:\t" + htmlfile + "\n\n"
                Makefile = Makefile + "index:\t" + indexfile + "\n\n"
                Makefile = Makefile + "txt:\t" + txtfile + "\n\n"
                Makefile = Makefile + "omf:\t" + omffile + "\n\n"

                if file.format_code=='sgml' and doc.dtd_code=='LinuxDoc':
                    Makefile = Makefile + dbsgmlfile + ':\t' + file.file_only + '\n'
                    Makefile = Makefile + '\t$(BUILD_DOCBOOK)\n\n'
                    Makefile = Makefile + xmlfile + ":\t" + dbsgmlfile + "\n"
                    Makefile = Makefile + "\t$(BUILD_XML)\n\n"
                else:
                    Makefile = Makefile + xmlfile + ":\t" + file.file_only + "\n"
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
                if doc.format_code<>'xml':
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
        docbookmake = ''
        xmlmake = ''
        htmlmake = ''
        indexmake = ''
        txtmake = ''
        omfmake = ''
        cleanmake = ''
        rebuildmake = ''
        makeneeded = 0
        for docid in lampadas.docs.keys():
            doc = lampadas.docs[docid]
            if doc.errors.count()==0 and doc.files.error_count()==0:
                for file in doc.files.keys():
                    file = doc.files[file]
                    if file.top==1:
    #                    if (file.format_code=='sgml' and doc.dtd_code=='DocBook') or (file.format_code=='sgml' and doc.dtd_code=='LinuxDoc') or file.format_code=='xml' or file.format_code=='wikitext' or file.format_code=='text':
                        makeneeded = 1
                        docsmake = docsmake + "\tcd " + str(docid) + "; $(MAKE) all 2>>make.log\n"
                        docbookmake = docbookmake + '\tcd ' + str(docid) + '; $(MAKE) xml 2>>make.log\n'
                        xmlmake = xmlmake + "\tcd " + str(docid) + "; $(MAKE) xml 2>>make.log\n"
                        htmlmake = htmlmake + "\tcd " + str(docid) + "; $(MAKE) html 2>>make.log\n"
                        indexmake = indexmake + "\tcd " + str(docid) + "; $(MAKE) index 2>>make.log\n"
                        txtmake = txtmake + "\tcd " + str(docid) + "; $(MAKE) txt 2>>make.log\n"
                        omfmake = omfmake + "\tcd " + str(docid) + "; $(MAKE) omf 2>>db2omf.log\n"
                        cleanmake = cleanmake + "\tcd " + str(docid) + "; $(MAKE) clean 2>>make.log\n"
                        rebuildmake = rebuildmake + "\tcd " + str(docid) + "; $(MAKE) rebuild 2>>make.log\n"

        if makeneeded:
            Makefile = "all:\tbuild\n\n"
            Makefile = Makefile + "build:\tdocs\n\n"
            Makefile = Makefile + "docs:\n" + docsmake + "\n\n"
            Makefile = Makefile + "docbook:\n" + docbookmake + "\n\n"
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
    print "Running Makefile on all documents..."
    makefile.write_all()

