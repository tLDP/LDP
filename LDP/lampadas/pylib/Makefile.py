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

from BaseClasses import *
from Globals import *
from DataLayer import lampadas
from SourceFiles import sourcefiles
from Config import config
from Lintadas import lintadas
from Log import log
import sys
from types import *


# Constants

XSLTPROC_PARAMS = ''

def add_items(data, items):
    if type(items) is StringType:
        data[items] = SortBy(len(data) + 1)
    elif type(items) is ListType:
        for item in items:
            data[item] = SortBy(len(data) + 1)
    else:
        print 'ERROR: Unrecognized type: ' + str(items)
        sys.exit(1)


# Special little nothing class to hold just a sort key.

class SortBy:

    def __init__(self, sort_by):
        self.sort_by = sort_by


# Dependencies

class Dependencies(LampadasCollection):

    def __init__(self, items=[]):
        self.data = {}
        add_items(self.data, items)
        
    def add(self, items):
        add_items(self.data, items)

    def get_text(self):
        text = ''
        for key in self.sort_by('sort_by'):
            if text=='':
                text += '\t' + key
            else:
                text = text + ' ' + key
        text += '\n'
        return text


# Commands

class Commands(LampadasCollection):

    def __init__(self, items=[]):
        self.data = {}
        add_items(self.data, items)

    def add(self, items):
        add_items(self.data, items)
    
    def get_text(self):
        text = ''
        for key in self.sort_by('sort_by'):
            text = text + '\t' + key + '\n'
        return text


# Targets

class Targets(LampadasCollection):

    def __init__(self):
        self.data = {}
        self.counter = 0

    def add(self, name, dependencies=[], commands=[]):
        self.counter        = self.counter + 1
        target              = Target()
        target.name         = name
        target.dependencies = Dependencies(dependencies)
        target.commands     = Commands(commands)
        target.sort_order   = self.counter
        self.data[name] = target
        return target
        
class Target:

    def __init__(self, name='', dependencies=[], commands=[]):
        self.name         = name
        self.dependencies = Dependencies(dependencies)
        self.commands     = Commands(commands)


# Project

class Project:

    def __init__(self):
        self.filename = ''
        self.targets  = Targets()
        
    def write(self, filename):
        contents = ''
        for key in self.targets.sort_by('sort_order'):
            target = self.targets[key]
            contents += target.name + ':'
            contents += target.dependencies.get_text()
            contents += target.commands.get_text()
            contents += '\n'
        fh = open(filename, 'w')
        fh.write(contents)
        fh.close


# Old version

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
        workdir   = config.cache_dir + str(doc.id) + '/work/'
        self.write_makefile(doc, workdir)
        
        log(3, 'Writing Makefile for document ' + str(doc_id) + ' complete.')
        

    def write_makefile(self, doc, dir):
        """
        Writes a Makefile to convert the source files into DocBook XML.
        """

        # If the file is not publishable (Archived or Normal status), skip it
        if doc.errors.count() > 0 or (doc.pub_status_code<>'A' and doc.pub_status_code<>'N'):
            return

        for file in doc.files.keys():
            docfile = doc.files[file]
            sourcefile = sourcefiles[file]
            if docfile.top==1 and sourcefile.errors.count()==0:
                log(3, 'Found top file: ' + sourcefile.filename)
                
                dbsgmlfile      = sourcefile.dbsgmlfile
                xmlfile         = sourcefile.xmlfile
                utfxmlfile      = sourcefile.utfxmlfile
                utftempxmlfile  = sourcefile.utftempxmlfile
                tidyxmlfile     = sourcefile.tidyxmlfile
                htmlfile        = sourcefile.htmlfile
                indexfile       = sourcefile.indexfile
                txtfile         = sourcefile.txtfile
                omffile         = sourcefile.omffile

                # FIXME: Read this information from a configuration file,
                # so admins can configure how makefiles are written,
                # and create their own targets, that suit their project.

                project = Project()
                project.filename = sourcefile.file_only
                project.targets.add('all', 'build')
                project.targets.add('publish', ['build', '../' + xmlfile, '../' + htmlfile, '../' + indexfile, '../' + txtfile, '../' + omffile])
                project.targets.add('../' + xmlfile,  tidyxmlfile, 'cp -up ' + tidyxmlfile + ' ../' + xmlfile)
                project.targets.add('../' + htmlfile, htmlfile,    'cp -up *.html ..')
                project.targets.add('../' + txtfile,  txtfile,     'cp -up ' + txtfile + ' ..')
                project.targets.add('../' + omffile,  omffile,     'cp -up ' + omffile + ' ..')
                project.targets.add('unpublish', [],
                                    ['rm -f ../*.html',
                                     'rm -f ../' + xmlfile,
                                     'rm -f ../' + txtfile,
                                     'rm -f ../' + omffile])
                project.targets.add('rebuild', ['clean', 'build'])
                project.targets.add('build', ['dbsgml', 'xml', 'tidyxml', 'html', 'index', 'txt', 'omf'])
                target = project.targets.add('clean', [],
                                             ['rm -f ' + txtfile,
                                             'rm -f ' + dbsgmlfile,
                                             'rm -f expanded.sgml',
                                             'rm -f expanded.fot',
                                             'rm -f ' + xmlfile,
                                             'rm -f ' + omffile,
                                             'rm -f log/*'])
                if sourcefile.format_code<>'txt':
                    target.commands.add('rm -f ' + txtfile)
                if sourcefile.format_code<>'html':
                    target.commands.add('rm -f *.html')
                if sourcefile.format_code<>'xml':
                    target.commands.add('rm -f *.xml')

                # Pseudotargets
                project.targets.add('dbsgml',  dbsgmlfile)
                project.targets.add('xml',     xmlfile)
                project.targets.add('utfxml',  utfxmlfile)
                project.targets.add('tidyxml', tidyxmlfile)
                project.targets.add('html',    htmlfile)
                project.targets.add('index',   indexfile)
                project.targets.add('txt',     txtfile)
                project.targets.add('omf',     omffile)

                if sourcefile.format_code=='wikitext':
                    project.targets.add(dbsgmlfile, sourcefile.file_only, 'wt2db -n -s ' + dbsgmlfile + ' -o ' + sourcefile.file_only + ' 2>>log/wt2db.log')
                    project.targets.add(xmlfile, dbsgmlfile, 'xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + ' 2>>log/xmllint.log')
                elif sourcefile.format_code=='txt':
                    project.targets.add(dbsgmlfile, sourcefile.file_only, 'wt2db -n -s ' + dbsgmlfile + ' -o ' + sourcefile.file_only + ' 2>>wt2db.log')
                    project.targets.add(xmlfile, dbsgmlfile, 'xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + ' 2>>log/xmllint.log')
                elif sourcefile.format_code=='texinfo':
                    project.targets.add(dbsgmlfile, sourcefile.file_only, 'texi2db -f ' + sourcefile.file_only + ' 2>>texi2db.log')
                    project.targets.add(xmlfile, dbsgmlfile, 'xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + ' 2>>log/xmllint.log')
                elif sourcefile.format_code=='sgml' and sourcefile.dtd_code=='LinuxDoc':
                    project.targets.add(dbsgmlfile, sourcefile.file_only, ['sgmlnorm -d /usr/local/share/ld2db/docbook.dcl ' + sourcefile.file_only + ' > expanded.sgml 2>>log/sgmlnorm.log',
                                                                         'jade -t sgml -c /usr/local/share/ld2db/catalog -d /usr/local/share/ld2db/ld2db.dsl\\#db expanded.sgml > ' + dbsgmlfile + ' 2>>log/jade.log'])
                    project.targets.add(xmlfile, dbsgmlfile, 'xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + ' 2>>log/xmllint.log')
                elif sourcefile.format_code=='sgml' and sourcefile.dtd_code=='DocBook':
                    project.targets.add(dbsgmlfile, sourcefile.file_only)
                    project.targets.add(xmlfile, sourcefile.file_only, 'xmllint --sgml ' + sourcefile.file_only + ' > ' + xmlfile + ' 2>>log/xmllint.log')
                elif sourcefile.format_code=='xml' and sourcefile.dtd_code=='DocBook':
                    project.targets.add(dbsgmlfile)
                    project.targets.add(xmlfile)
                
                # Everybody gets encoded into UTF-8 here
                project.targets.add(utfxmlfile, xmlfile, ['iconv -f ISO-8859-1  -t UTF-8 ' + xmlfile + ' > ' + utftempxmlfile + ' 2>>log/iconv.log',
                                                                 'xmllint --encode UTF-8 ' + utftempxmlfile + ' > ' + utfxmlfile + ' 2>>log/xmllint.log'])
                # Everybody gets xml tidied before processing further
                project.targets.add(tidyxmlfile, utfxmlfile, 'tidy -config /etc/lampadas/tidyrc -quiet -f log/tidy.log ' + utfxmlfile + ' > ' + tidyxmlfile + ' 2>>log/tidy.log')

                # Now we have good DocBook XML, generate all outputs
                project.targets.add(htmlfile, tidyxmlfile, 'xsltproc --param quiet 1 --maxdepth 100 ' + XSLTPROC_PARAMS + ' ' + config.xslt_html + ' ' + tidyxmlfile + ' > ' + htmlfile + ' 2>>log/xsltproc.log')
                project.targets.add(indexfile, tidyxmlfile, 'xsltproc --param quiet 1 --maxdepth 100 ' + XSLTPROC_PARAMS + ' ' + config.xslt_chunk + ' ' + tidyxmlfile + ' > ' + indexfile + ' 2>>log/xsltproc.log')
                project.targets.add(omffile, tidyxmlfile, 'db2omf ' + tidyxmlfile + ' -o ' + omffile + ' 2>>log/db2omf.log')
                project.targets.add(txtfile, htmlfile, 'lynx --dump --nolist ' + htmlfile + ' > ' + txtfile + ' 2>>log/lynx.log')
                
                # Write the Makefile to disk
                project.write(dir + 'Makefile')

                

    def write_main_makefile(self):
        publishmake = ''
        unpublishmake = ''
        rebuildmake = ''
        buildmake = ''
        cleanmake = ''
        tidyxmlmake = ''
        htmlmake = ''
        indexmake = ''
        txtmake = ''
        omfmake = ''

        makeneeded = 0
        for docid in lampadas.docs.keys():
            doc = lampadas.docs[docid]
            if doc.errors.count()==0 and doc.files.error_count==0:
                for file in doc.files.keys():
                    docfile = doc.files[file]
                    sourcefile = sourcefiles[file]
                    if docfile.top==1:
                        makeneeded = 1
                        publishmake   = "\tcd " + str(docid) + "/work; $(MAKE) publish 2>>log/publish.log\n"     + publishmake       
                        unpublishmake = "\tcd " + str(docid) + "/work; $(MAKE) unpublish 2>>log/unpublish.log\n" + unpublishmake       
                        rebuildmake   = "\tcd " + str(docid) + "/work; $(MAKE) rebuild 2>>log/make.log\n"        + rebuildmake   
                        buildmake     = "\tcd " + str(docid) + "/work; $(MAKE) all 2>>log/make.log\n"            + buildmake     
                        cleanmake     = "\tcd " + str(docid) + "/work; $(MAKE) clean 2>>log/make.log\n"          + cleanmake     
                        tidyxmlmake   = "\tcd " + str(docid) + "/work; $(MAKE) tidyxml 2>>log/make.log\n"        + tidyxmlmake   
                        htmlmake      = "\tcd " + str(docid) + "/work; $(MAKE) html 2>>log/make.log\n"           + htmlmake      
                        indexmake     = "\tcd " + str(docid) + "/work; $(MAKE) index 2>>log/make.log\n"          + indexmake     
                        txtmake       = "\tcd " + str(docid) + "/work; $(MAKE) txt 2>>log/make.log\n"            + txtmake      
                        omfmake       = "\tcd " + str(docid) + "/work; $(MAKE) omf 2>>log/db2omf.log\n"          + omfmake       

        if makeneeded:
            Makefile = "all:\tbuild\n\n"
            Makefile = Makefile + "publish:\n"   + publishmake + "\n\n"
            Makefile = Makefile + "unpublish:\n" + unpublishmake + "\n\n"
            Makefile = Makefile + "rebuild:\n"   + rebuildmake + "\n\n"
            Makefile = Makefile + "build:\n"     + buildmake + "\n\n"
            Makefile = Makefile + "clean:\n"     + cleanmake + "\n\n"
            Makefile = Makefile + "tidyxml:\n"   + tidyxmlmake + "\n\n"
            Makefile = Makefile + "html:\n"      + htmlmake + "\n\n"
            Makefile = Makefile + "index:\n"     + indexmake + "\n\n"
            Makefile = Makefile + "txt:\n"       + txtmake + "\n\n"
            Makefile = Makefile + "omf:\n"       + omfmake + "\n\n"

            fh = open(config.cache_dir + 'Makefile', 'w')
            fh.write(Makefile)
            fh.close


makefile = Makefile()


if __name__=="__main__":
#    print "Writing Makefiles for all documents..."
#    makefile.write(4)
    makefile.write_all()

