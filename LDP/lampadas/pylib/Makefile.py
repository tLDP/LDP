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


# Globals

def add_items(data, items):
    if type(items) is StringType:
        data[items] = SortOrder(len(data) + 1)
    elif type(items) is ListType:
        for item in items:
            data[item] = SortOrder(len(data) + 1)
    else:
        print 'ERROR: Unrecognized type: ' + str(items)
        sys.exit(1)


# Special little nothing class to hold just a sort key.

class SortOrder:

    def __init__(self, sort_order):
        self.sort_order = sort_order


# Dependencies

class Dependencies(LampadasCollection):

    def __init__(self, items=[]):
        self.data = {}
        add_items(self.data, items)
        
    def add(self, items):
        add_items(self.data, items)

    def get_text(self):
        text = ''
        for key in self.sort_by('sort_order'):
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
        for key in self.sort_by('sort_order'):
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
        target.timestamp    = ''
        self.data[name] = target
        return target
       
class Target:

    def __init__(self, name='', dependencies=[], commands=[]):
        self.name         = name
        self.dependencies = Dependencies(dependencies)
        self.commands     = Commands(commands)
        self.timestamp    = ''


# Projects

class Projects(LampadasCollection):

    def __init__(self):
        self.data = {}
        for key in lampadas.docs.keys():
            project = Project(key)
            self.data[key] = project
        
    def make_target(self, name='all'):
        log(3, 'Running project Makefile target: ' + name)
        for doc_id in self.sort_by('doc_id'):
            self[doc_id].make_target(name)

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
        self.workdir = config.cache_dir + str(self.doc_id) + '/work/'
        self.filename = ''
        self.targets  = Targets()
        self.pub_times = LampadasCollection()
        self.doc = lampadas.docs[doc_id]
        
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
                self.targets.add('all', 'build')
                self.targets.add('republish', ['clean', 'build', 'unpublish', 'publish'])
                self.targets.add('publish', ['build', '../' + xmlfile, '../' + htmlfile, '../' + indexfile, '../' + txtfile, '../' + omffile])
                self.targets.add('../' + xmlfile,  tidyxmlfile, 'cp -up ' + tidyxmlfile + ' ../' + xmlfile)
                self.targets.add('../' + htmlfile, htmlfile,    'cp -up *.html ..')
                self.targets.add('../' + indexfile, indexfile,  'cp -up ' + indexfile + '..')
                self.targets.add('../' + txtfile,  txtfile,     'cp -up ' + txtfile   + ' ..')
                self.targets.add('../' + omffile,  omffile,     'cp -up ' + omffile   + ' ..')
                self.targets.add('unpublish', [],
                                    ['rm -f ../*.html',
                                     'rm -f ../' + xmlfile,
                                     'rm -f ../' + txtfile,
                                     'rm -f ../' + omffile])
                self.targets.add('rebuild', ['clean', 'build'])
                self.targets.add('build', ['dbsgml', 'xml', 'tidyxml', 'html', 'index', 'txt', 'omf'])
                target = self.targets.add('clean', [],
                                            ['rm -f log/*',
                                             'rm -f expanded.sgml',
                                             'rm -f expanded.fot',
                                             'rm -f ' + dbsgmlfile,
                                             'rm -f ' + xmlfile,
                                             'rm -f ' + omffile,
                                             'rm -f ' + txtfile])
                if sourcefile.format_code<>'txt':
                    target.commands.add('rm -f ' + txtfile)
                if sourcefile.format_code<>'html':
                    target.commands.add('rm -f *.html')
                if sourcefile.format_code<>'xml':
                    target.commands.add('rm -f *.xml')

                if sourcefile.format_code=='wikitext':
                    self.targets.add(dbsgmlfile, sourcefile.file_only, 'wt2db -n -s ' + dbsgmlfile + ' -o ' + sourcefile.file_only + ' 2>>log/wt2db.log')
                    self.targets.add(xmlfile, dbsgmlfile, 'xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + ' 2>>log/xmllint.log')
                elif sourcefile.format_code=='txt':
                    self.targets.add(dbsgmlfile, sourcefile.file_only, 'wt2db -n -s ' + dbsgmlfile + ' -o ' + sourcefile.file_only + ' 2>>wt2db.log')
                    self.targets.add(xmlfile, dbsgmlfile, 'xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + ' 2>>log/xmllint.log')
                elif sourcefile.format_code=='texinfo':
                    self.targets.add(dbsgmlfile, sourcefile.file_only, 'texi2db -f ' + sourcefile.file_only + ' 2>>texi2db.log')
                    self.targets.add(xmlfile, dbsgmlfile, 'xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + ' 2>>log/xmllint.log')
                elif sourcefile.format_code=='sgml' and sourcefile.dtd_code=='LinuxDoc':
                    self.targets.add(dbsgmlfile, sourcefile.file_only, ['sgmlnorm -d /usr/local/share/ld2db/docbook.dcl ' + sourcefile.file_only + ' > expanded.sgml 2>>log/sgmlnorm.log',
                                                                         'jade -t sgml -c /usr/local/share/ld2db/catalog -d /usr/local/share/ld2db/ld2db.dsl\\#db expanded.sgml > ' + dbsgmlfile + ' 2>>log/jade.log'])
                    self.targets.add(xmlfile, dbsgmlfile, 'xmllint --sgml ' + dbsgmlfile + ' > ' + xmlfile + ' 2>>log/xmllint.log')
                elif sourcefile.format_code=='sgml' and sourcefile.dtd_code=='DocBook':
                    self.targets.add(dbsgmlfile, sourcefile.file_only)
                    self.targets.add(xmlfile, sourcefile.file_only, 'xmllint --sgml ' + sourcefile.file_only + ' > ' + xmlfile + ' 2>>log/xmllint.log')
                elif sourcefile.format_code=='xml' and sourcefile.dtd_code=='DocBook':
                    self.targets.add(dbsgmlfile)
                    self.targets.add(xmlfile)
                
                # Everybody gets encoded into UTF-8 here
                self.targets.add(utfxmlfile, xmlfile, ['iconv -f ISO-8859-1  -t UTF-8 ' + xmlfile + ' > ' + utftempxmlfile + ' 2>>log/iconv.log',
                                                                 'xmllint --encode UTF-8 ' + utftempxmlfile + ' > ' + utfxmlfile + ' 2>>log/xmllint.log'])
                # Everybody gets xml tidied before processing further
                self.targets.add(tidyxmlfile, utfxmlfile, 'tidy -config /etc/lampadas/tidyrc -quiet -f log/tidy.log ' + utfxmlfile + ' > ' + tidyxmlfile + ' 2>>log/tidy.log')

                # Now we have good DocBook XML, generate all outputs
                self.targets.add(htmlfile, tidyxmlfile, 'xsltproc --param quiet 1 --maxdepth 100 ' + XSLTPROC_PARAMS + ' ' + config.xslt_html + ' ' + tidyxmlfile + ' > ' + htmlfile + ' 2>>log/xsltproc.log')
                self.targets.add(indexfile, tidyxmlfile, 'xsltproc --param quiet 1 --maxdepth 100 ' + XSLTPROC_PARAMS + ' ' + config.xslt_chunk + ' ' + tidyxmlfile + ' > ' + indexfile + ' 2>>log/xsltproc.log')
                self.targets.add(omffile, tidyxmlfile, 'db2omf ' + tidyxmlfile + ' -o ' + omffile + ' 2>>log/db2omf.log')
                self.targets.add(txtfile, htmlfile, 'lynx --dump --nolist ' + htmlfile + ' > ' + txtfile + ' 2>>log/lynx.log')

                # Calculate pseudotargets last, so they will have the file's
                # timestampe preloaded and available to them.
                self.targets.add('dbsgml',  dbsgmlfile)
                self.targets.add('xml',     xmlfile)
                self.targets.add('utfxml',  utfxmlfile)
                self.targets.add('tidyxml', tidyxmlfile)
                self.targets.add('html',    htmlfile)
                self.targets.add('index',   indexfile)
                self.targets.add('txt',     txtfile)
                self.targets.add('omf',     omffile)

    def make_target(self, name='all'):
        """
        Runs the Makefile specified target (defaulting to all)
        and records results as errors and other status flags
        against the document. Currently, the tables and fields
        affected are:

        If the document already has errors recorded against it,
        then it cannot be processed, and this routine will abort.
        
        Because this routine does not clear errors, any errors
        we set here will only be cleared by the Lintadas process.
        To summarize, this module ONLY records processing errors,
        and Lintadas ONLY clears them.
        """

        # This check needs to stay at the top of the routine.
        # 
        # Do not publish any document tagged with errors.
        # You can write a Makefile, but you cannot actually
        # execute the build through this mechanism. This is a
        # safety precaution.
        if self.doc.errors.count() > 0 or self.doc.files.error_count > 0:
            return 0

        # Do not publish any document which has not yet been mirrored.
        if self.doc.mirror_time=='':
            return 0

        # If there is no pub_time set and the target is a file,
        # read the file's timestamp and remember it.
        if self.pub_times[name]==None:
            if os.access(self.workdir + name, os.F_OK)<>0:
                os_stat = os.stat(self.workdir + name)
                time_value = os_stat[stat.ST_MTIME]
                time_tuple = time.gmtime(time_value)
                pub_time = time.strftime('%Y-%m-%d %H:%M:%S', time_tuple)
                print name + ' pub_time: ' + pub_time
                self.pub_times[name] = pub_time
                return 0
                
            # Identify when we hit a source file and begin recursing out.
            else:
                target = self.targets[name]
                if target==None:
                    print 'ERROR: Cannot locate target file: ' + name
                    self.doc.errors.add(ERR_MAKE_NO_SOURCE)
                    return -1

        # If we've already processed this target, don't do it all over again.
        else:
            return 0

        # Build the target
        target = self.targets[name]
        if target==None:
            print 'ERROR: Cannot find target ' + name + ', and it was not a file.'
            sys.exit(1)

        #print 'Processing target: ' + name
        # First make sure all dependencies are caught up.
        exit_status = 0
        for key in target.dependencies.sort_by('sort_order'):
            #print 'Found dependency: ' + name + ': ' +  key
            exit_status = self.make_target(key)
            if exit_status<>0:
                break
                
        # Run this level's commands if all of the dependencies built
        # without triggering any errors.
        if exit_status==0:
        
            # Some targets, when successfully made,
            # are recorded in the document's meta-data.
            # Most are not. Those which are recorded are:
            # 
            #   publish:    set to now_string()
            #   unpublish:  set to ''
            # 
            # Assume for now that the build will be successful,
            # and override later if an error occurs.
            if name=='publish':
                self.doc.pub_time = now_string()
            elif name=='unpublish':
                self.doc.pub_time = ''

            # Build the target by iterating through its commands.
            # If this target is a file and a dependency is also a file,
            # do not execute the dependency.
            #print 'All dependencies for ' + name +  ' built, building target...'
            for key in target.commands.sort_by('sort_order'):
                command = 'cd ' + self.workdir + '; ' + key
                #print 'Running command: ' + command
                print '\t' + command
                exit_status = os.system(command)

                # Flag exit status error at the point where the exit_status
                # changes state from 0 to 1 due to command failure.
                if exit_status<>0:
                    self.doc.errors.add(ERR_MAKE_EXIT_STATUS)
                    print 'ERR_MAKE_EXIT_STATUS: ' + command
                    if name=='publish':
                        self.doc.pub_time = ''
                    elif name=='unpublish':
                        self.doc.pub_time = ''
                    break

        self.doc.save()
        return exit_status
    
    # FIXME: Add a way to customize the makefile for a document.
    # Maybe we could just have a way to disable overwriting the
    # Makefile on a document-by-document basis.

    def write(self):
        """Writes the contents of a regular Makefile to disk."""
        
        contents = ''
        for key in self.targets.sort_by('sort_order'):
            target = self.targets[key]
            contents += target.name + ':'
            contents += target.dependencies.get_text()
            contents += target.commands.get_text()
            contents += '\n'
        fh = open(self.workdir + 'Makefile', 'w')
        fh.write(contents)
        fh.close


projects = Projects()


if __name__=="__main__":
    print "Writing Makefiles for all documents..."
    projects.write()
    projects.write_main()
    projects.make_target('publish')

# Some old test code.
# It's useful when debugging so I'm leaving it here.
# 
#    for i in range(5):
#        doc_id = i + 1
#        print "Writing Makefiles for document " + str(doc_id)
#        project = projects[i + 1]
#        if project==None:
#            print 'ERROR: Cannot find project: ' + str(doc_id)
#            sys.exit(1)
#        else:
#            project.make_target('publish')

#    projects[4].make_target('clean')
#    projects[4].make_target('unpublish')
#    projects[4].make_target('publish')
#    projects[4].make_target('html')


