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

# Constants

XSLTPROC_PARAMS = ''


# Modules ##################################################################

from BaseClasses import *
from Globals import *
from DataLayer import lampadas
from SourceFiles import sourcefiles
from Config import config
from Lintadas import lintadas
from Log import log
import sys
import os
import stat
import time
from types import *


# Targets

class Targets(LampadasCollection):

    def add(self, name, dependencies, commands):
        target = Target(name, dependencies, commands)
        target.sort_order = len(self.data) + 1
        self.data[target.name] = target
        return target
       
class Target:

    def __init__(self, name, dependencies, commands):
        self.name         = name
        self.dependencies = dependencies
        self.commands     = commands

    def get_text(self):
        dep_text = ''
        for key in self.dependencies:
            if dep_text=='':
                dep_text = '\t' + key
            else:
                dep_text = dep_text + ' ' + key
        dep_text = dep_text + '\n'
        cmd_text = ''
        for key in self.commands:
            if cmd_text=='':
                cmd_text = '\t' + key
            else:
                cmd_text = cmd_text + ' ' + key
        return dep_text + cmd_text


# Projects

class Projects(LampadasCollection):

    def __init__(self):
        self.data = {}
        for key in lampadas.docs.sort_by('id'):
            project = Project(key)
            self.data[key] = project
        
    def make(self, name='all'):
        log(3, 'Running project Makefile target: ' + name)
        for doc_id in self.sort_by('doc_id'):
            print 'Building document: ' + str(doc_id)
            self[doc_id].make(name)

    def write(self):
        log(3, 'Writing Makefile for all documents')
        for doc_id in self.keys():
            self[doc_id].write()

    def write_main(self):
        republishmake = ''
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

            # Do not make documents with errors filed against them.
            if doc.errors.count() > 0 or doc.files.error_count > 0:
                continue
            
            # Make each individual file
            for file in doc.files.keys():
                docfile = doc.files[file]
                sourcefile = sourcefiles[file]
                if docfile.top==1:
                    makeneeded = 1
                    republishmake = "\tcd " + str(docid) + "/work; $(MAKE) republish 2>>log/republish.log\n" + republishmake       
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
            Makefile = Makefile + "republish:\n" + republishmake + "\n\n"
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

class Project:

    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.doc = lampadas.docs[doc_id]
        self.workdir = config.cache_dir + str(self.doc_id) + '/work/'
        self.filename = ''
        self.targets  = Targets()
        
        # If the file is not publishable (Archived or Normal status), skip it
        if self.doc.errors.count() > 0 or self.doc.files.error_count > 0 or (self.doc.pub_status_code<>'A' and self.doc.pub_status_code<>'N'):
            return

        for file in self.doc.files.keys():
            docfile = self.doc.files[file]
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

                self.filename = sourcefile.file_only
                self.targets.add('all',             ['build'],          [])
                self.targets.add('republish',       ['clean', 'build', 'unpublish', 'publish'], [])
                self.targets.add('publish',         ['build', '../' + xmlfile, '../' + htmlfile, '../' + indexfile, '../' + txtfile, '../' + omffile], [])
                self.targets.add('../' + xmlfile,   [tidyxmlfile],      ['cp -up ' + tidyxmlfile + ' ../' + xmlfile])
                self.targets.add('../' + htmlfile,  [htmlfile],         ['cp -up *.html ..'])
                self.targets.add('../' + indexfile, [indexfile],        ['cp -up ' + indexfile + '..'])
                self.targets.add('../' + txtfile,   [txtfile],          ['cp -up ' + txtfile   + ' ..'])
                self.targets.add('../' + omffile,   [omffile],          ['cp -up ' + omffile   + ' ..'])
                self.targets.add('unpublish',       [],                 ['rm -f ../*.html', 'rm -f ../' + xmlfile, 'rm -f ../' + txtfile, 'rm -f ../' + omffile])
                self.targets.add('rebuild',         ['clean', 'build'], [])
                self.targets.add('build', ['dbsgml', 'xml', 'tidyxml', 'html', 'index', 'txt', 'omf'], [])
                target = self.targets.add('clean', [],
                                            ['rm -f log/*',
                                             'rm -f expanded.sgml',
                                             'rm -f expanded.fot',
                                             'rm -f ' + dbsgmlfile,
                                             'rm -f ' + xmlfile,
                                             'rm -f ' + omffile,
                                             'rm -f ' + txtfile])
                if sourcefile.format_code<>'txt':
                    target.commands += ['rm -f ' + txtfile]
                if sourcefile.format_code<>'html':
                    target.commands += ['rm -f *.html']
                if sourcefile.format_code<>'xml':
                    target.commands += ['rm -f *.xml']

                if sourcefile.format_code=='wikitext':
                    self.targets.add(dbsgmlfile, [sourcefile.file_only], ['wt2db -n -s ' + dbsgmlfile + ' -o ' + sourcefile.file_only + ' 2>>log/wt2db.log'])
                    self.targets.add(xmlfile,    [dbsgmlfile],           ['xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + ' 2>>log/xmllint.log'])
                elif sourcefile.format_code=='txt':
                    self.targets.add(dbsgmlfile, [sourcefile.file_only], ['wt2db -n -s ' + dbsgmlfile + ' -o ' + sourcefile.file_only + ' 2>>wt2db.log'])
                    self.targets.add(xmlfile,    [dbsgmlfile],           ['xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + ' 2>>log/xmllint.log'])
                elif sourcefile.format_code=='texinfo':
                    self.targets.add(dbsgmlfile, [sourcefile.file_only], ['texi2db -f ' + sourcefile.file_only + ' 2>>texi2db.log'])
                    self.targets.add(xmlfile,    [dbsgmlfile],           ['xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + ' 2>>log/xmllint.log'])
                elif sourcefile.format_code=='sgml' and sourcefile.dtd_code=='LinuxDoc':
                    self.targets.add(dbsgmlfile, [sourcefile.file_only], ['sgmlnorm -d /usr/local/share/ld2db/docbook.dcl ' + sourcefile.file_only + ' > expanded.sgml 2>>log/sgmlnorm.log',
                                                                          'jade -t sgml -c /usr/local/share/ld2db/catalog -d /usr/local/share/ld2db/ld2db.dsl\\#db expanded.sgml > ' + dbsgmlfile + ' 2>>log/jade.log'])
                    self.targets.add(xmlfile,    [dbsgmlfile],           ['xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + ' 2>>log/xmllint.log'])
                elif sourcefile.format_code=='sgml' and sourcefile.dtd_code=='DocBook':
                    self.targets.add(dbsgmlfile, [sourcefile.file_only], [])
                    self.targets.add(xmlfile,    [sourcefile.file_only], ['xmllint --sgml ' + sourcefile.file_only + ' > ' + xmlfile + ' 2>>log/xmllint.log'])
                elif sourcefile.format_code=='xml' and sourcefile.dtd_code=='DocBook':
                    self.targets.add(dbsgmlfile, [],                     [])
                    self.targets.add(xmlfile,    [],                     [])
                
                # Everybody gets encoded into UTF-8 here
                self.targets.add(utfxmlfile,     [xmlfile],              ['iconv -f ISO-8859-1  -t UTF-8 ' + xmlfile + ' > ' + utftempxmlfile + ' 2>>log/iconv.log',
                                                                          'xmllint --encode UTF-8 ' + utftempxmlfile + ' > ' + utfxmlfile + ' 2>>log/xmllint.log'])
                # Everybody gets xml tidied before processing further
                self.targets.add(tidyxmlfile,    [utfxmlfile],           ['tidy -config /etc/lampadas/tidyrc -quiet -f log/tidy.log ' + utfxmlfile + ' > ' + tidyxmlfile + ' 2>>log/tidy.log'])

                # Now we have good DocBook XML, generate all outputs
                self.targets.add(htmlfile,       [tidyxmlfile],          ['xsltproc --param quiet 1 --maxdepth 100 ' + XSLTPROC_PARAMS + ' ' + config.xslt_html + ' ' + tidyxmlfile + ' > ' + htmlfile + ' 2>>log/xsltproc.log'])
                self.targets.add(indexfile,      [tidyxmlfile],          ['xsltproc --param quiet 1 --maxdepth 100 ' + XSLTPROC_PARAMS + ' ' + config.xslt_chunk + ' ' + tidyxmlfile + ' > ' + indexfile + ' 2>>log/xsltproc.log'])
                self.targets.add(omffile,        [tidyxmlfile],          ['db2omf ' + tidyxmlfile + ' -o ' + omffile + ' 2>>log/db2omf.log'])
                self.targets.add(txtfile,        [htmlfile],             ['lynx --dump --nolist ' + htmlfile + ' > ' + txtfile + ' 2>>log/lynx.log'])

                # Calculate pseudotargets last, so they will have the file's
                # timestampe preloaded and available to them.
                self.targets.add('dbsgml',       [dbsgmlfile],           [])
                self.targets.add('xml',          [xmlfile],              [])
                self.targets.add('utfxml',       [utfxmlfile],           [])
                self.targets.add('tidyxml',      [tidyxmlfile],          [])
                self.targets.add('html',         [htmlfile],             [])
                self.targets.add('index',        [indexfile],            [])
                self.targets.add('txt',          [txtfile],              [])
                self.targets.add('omf',          [omffile],              [])

    def make(self, name='all'):
        """
        Runs the makefile specified target (defaulting to all)
        and records errors, results and other status flags
        against the document.

        If the document already has errors recorded against it,
        then it cannot be processed, and this routine will abort.
        
        Because this routine does not clear errors, any errors
        we set here will only be cleared by the Lintadas process.
        to summarize, this module only records processing errors,
        and lintadas only clears them.
        """

        # do not publish any document tagged with errors,
        # or which has not yet been mirrored
        if self.doc.errors.count() > 0 or self.doc.files.error_count > 0 or self.doc.mirror_time=='':
            return

        # Build the target
        target = self.targets[name]
        high_timestamp = 0
        exit_status = 0

        # Build all dependencies, but abort if any one fails.
        if not target==None:
            for dep in target.dependencies:
                (exit_status, dep_timestamp) = self.make(dep)
                if dep_timestamp > high_timestamp:
                    high_timestamp = dep_timestamp
                if exit_status<>0:
                    return (exit_status, 0)

        # All dependencies are buil, so now this target
        # is ready to be built.
        # See if we can get a timestamp for ourself.
        # If not, just use 0.
        filename = self.workdir + name
        if os.access(filename, os.F_OK)<>0:
            os_stat = os.stat(filename)
            timestamp = os_stat[stat.ST_MTIME]
        else:
            timestamp = 0

        # Build if our timestamp is older.
        # Build if they match too, because we get a lot of 0's.
        if timestamp <= high_timestamp:
            print 'Building target: ' + name
            timestamp = time.time()
            for cmdkey in target.commands:
                command = 'cd ' + self.workdir + '; ' + cmdkey
                #print 'Running: ' + command
                exit_status = os.system(command)
                if exit_status<>0:
                    self.doc.errors.add(ERR_MAKE_EXIT_STATUS)
                    return(exit_status, timestamp)

            # Reread our timestamp. It's like to have changed.
            # If we still have no file, use wall time.
            filename = self.workdir + name
            if os.access(filename, os.F_OK)<>0:
                os_stat = os.stat(filename)
                timestamp = os_stat[stat.ST_MTIME]
            else:
                timestamp = time.time()

        # If we published or unpublished, we have to
        # update the data layer.
        if exit_status==0:
            if name=='publish':
                self.doc.pub_time = now_string()
            elif name=='unpublish':
                self.doc.pub_time = ''
        
        if high_timestamp > timestamp:
            timestamp = high_timestamp
        self.doc.save()
        return (exit_status, timestamp)
        
    
    # FIXME: Add a way to customize the makefile for a document.
    # Maybe we could just have a way to disable overwriting the
    # Makefile on a document-by-document basis.

    def write(self):
        """Writes the contents of a regular Makefile to disk."""
        
        contents = ''
        for key in self.targets.sort_by('sort_order'):
            target = self.targets[key]
            contents += target.name + ':'
            contents += target.get_text()
            contents += '\n'
        fh = open(self.workdir + 'Makefile', 'w')
        fh.write(contents)
        fh.close


projects = Projects()


if __name__=="__main__":
    print "Writing Makefiles for all documents..."
    projects.write()
    projects.write_main()
    projects.make('all')

