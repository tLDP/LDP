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

# Commands

class Commands(LampadasCollection):

    def add(self, command):
        command.sort_order = len(self.data) + 1
        self[command.sort_order] = command

class Command:

    def __init__(self, cmd_text, output_to='', errors_to='', stderr_check=0):
        self.command      = cmd_text
        self.output_to    = output_to
        self.errors_to    = errors_to
        self.stderr_check = stderr_check


# Targets

class Targets(LampadasCollection):

    def add(self, name, dependencies, commands):
        target = Target(name, dependencies, commands)
        target.sort_order = len(self.data) + 1
        self.data[target.name] = target
        return target
       
class Target:

    def __init__(self, name, dependencies, commands):
        """Initialize a target. Commands is a list of Command() objects."""

        self.name         = name
        self.dependencies = dependencies
        self.commands = Commands()
        for command in commands:
            self.commands.add(command)

    def get_text(self):
        dep_text = ''
        for key in self.dependencies:
            if dep_text=='':
                dep_text = '\t' + key
            else:
                dep_text = dep_text + ' ' + key
        dep_text = dep_text + '\n'
        cmd_text = ''
        for key in self.commands.sort_by('sort_order'):
            command = self.commands[key]
            if command.errors_to > '':
                cmd_text += '\trm -f ' + command.errors_to + '\n'
            cmd_text += '\t' 
            cmd_text += command.command
            if command.output_to > '':
                cmd_text += ' > ' + command.output_to
            if command.errors_to > '':
                cmd_text += ' 2>>' + command.errors_to
            cmd_text += '\n'
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
            doc = lampadas.docs[doc_id]
            if doc.pub_status_code<>'N':
                continue
            log(3, 'Making document: ' + str(doc_id))
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
            if doc.pub_time=='':
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
        self.doc_id = int(doc_id)
        self.doc = lampadas.docs[self.doc_id]
        self.workdir = config.cache_dir + str(self.doc_id) + '/work/'
        self.filename = ''
        self.targets  = Targets()
        
        # If the file is not to be published (Archived or Normal status),
        # or if it has not been mirrored successfully, skip it.
        if self.doc.pub_status_code<>'N'  or self.doc.mirror_time=='':
            return

        for file in self.doc.files.keys():
            docfile = self.doc.files[file]
            sourcefile = sourcefiles[file]
            
            if docfile.top==1:
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
                self.targets.add('republish',       ['unpublish', 'clean', 'build', 'publish'], [])
                self.targets.add('publish',         ['build', '../' + xmlfile, '../' + htmlfile, '../' + indexfile, '../' + txtfile, '../' + omffile], [])
                self.targets.add('../' + xmlfile,   [tidyxmlfile],      [Command('cp ' + tidyxmlfile + ' ../' + xmlfile)])
                self.targets.add('../' + htmlfile,  [htmlfile],         [Command('cp *.html ..')])
                self.targets.add('../' + indexfile, [indexfile],        [Command('cp ' + indexfile + ' ..')])
                self.targets.add('../' + txtfile,   [txtfile],          [Command('cp ' + txtfile   + ' ..')])
                self.targets.add('../' + omffile,   [omffile],          [Command('cp ' + omffile   + ' ..')])
                self.targets.add('unpublish',       [],                 [Command('rm -f ../*.html'), 
                                                                         Command('rm -f ../' + xmlfile),
                                                                         Command('rm -f ../' + txtfile),
                                                                         Command('rm -f ../' + omffile)])
                self.targets.add('rebuild',         ['clean', 'build'], [])
                self.targets.add('build', ['dbsgml', 'xml', 'tidyxml', 'html', 'index', 'txt', 'omf'], [])
                target = self.targets.add('clean', [],
                                            [Command('rm -f log/*'),
                                             Command('rm -f expanded.sgml'),
                                             Command('rm -f expanded.fot'),
                                             Command('rm -f ' + dbsgmlfile),
                                             Command('rm -f ' + xmlfile),
                                             Command('rm -f ' + omffile),
                                             Command('rm -f ' + txtfile)])
                if sourcefile.format_code<>'txt':
                    target.commands.add(Command('rm -f ' + txtfile))
                if sourcefile.format_code<>'html':
                    target.commands.add(Command('rm -f *.html'))
                if sourcefile.format_code<>'xml':
                    target.commands.add(Command('rm -f *.xml'))

                if sourcefile.format_code=='wikitext':
                    self.targets.add(dbsgmlfile, [sourcefile.file_only], [Command('wt2db -n -s ' + sourcefile.file_only + ' -o ' + dbsgmlfile, errors_to='log/wt2db.log', stderr_check=1)])
                    self.targets.add(xmlfile,    [dbsgmlfile],           [Command('xmllint --sgml ' + dbsgmlfile, output_to=xmlfile, errors_to='log/xmllint.log', stderr_check=1)])
                elif sourcefile.format_code=='text':
                    self.targets.add(dbsgmlfile, [sourcefile.file_only], [Command('wt2db -n -s ' + sourcefile.file_only + ' -o ' + dbsgmlfile, errors_to='log/wt2db.log', stderr_check=1)])
                    self.targets.add(xmlfile,    [dbsgmlfile],           [Command('xmllint --sgml ' + dbsgmlfile, output_to=xmlfile, errors_to='log/xmllint.log', stderr_check=1)])
                elif sourcefile.format_code=='texinfo':
                    self.targets.add(dbsgmlfile, [sourcefile.file_only], [Command('texi2db -f ' + sourcefile.file_only, errors_to='texi2db.log', stderr_check=1)])
                    self.targets.add(xmlfile,    [dbsgmlfile],           [Command('xmllint --sgml ' + dbsgmlfile, output_to=xmlfile, errors_to='log/xmllint.log', stderr_check=1)])
                elif sourcefile.format_code=='sgml' and sourcefile.dtd_code=='linuxdoc':
                    self.targets.add(dbsgmlfile, [sourcefile.file_only], [Command('sgmlnorm -d /usr/local/share/ld2db/docbook.dcl ' + sourcefile.file_only, output_to='expanded.sgml', errors_to='log/sgmlnorm.log', stderr_check=1),
                                                                          Command('jade -t sgml -c /usr/local/share/ld2db/catalog -d /usr/local/share/ld2db/ld2db.dsl\\#db expanded.sgml', output_to=dbsgmlfile, errors_to='log/jade.log', stderr_check=1)])
                    self.targets.add(xmlfile,    [dbsgmlfile],           [Command('xmllint --sgml ' + dbsgmlfile, output_to=xmlfile, errors_to='log/xmllint.log', stderr_check=1)])
                elif sourcefile.format_code=='sgml' and sourcefile.dtd_code=='docbook':
                    self.targets.add(dbsgmlfile, [sourcefile.file_only], [])
                    self.targets.add(xmlfile,    [sourcefile.file_only], [Command('xmllint --sgml ' + sourcefile.file_only, output_to=xmlfile, errors_to='log/xmllint.log', stderr_check=1)])
                elif sourcefile.format_code=='xml' and sourcefile.dtd_code=='docbook':
                    self.targets.add(dbsgmlfile, [],                     [])
                    self.targets.add(xmlfile,    [],                     [])
                else:
                    log(1, 'ERROR: Unrecognized format code/dtd_code: ' + sourcefile.format_code + '/' + sourcefile.dtd_code + '. Lampadas cannot build this document.')
                
                # Everybody gets encoded into UTF-8 here
                self.targets.add(utfxmlfile,     [xmlfile],              [Command('iconv -f ISO-8859-1  -t UTF-8 ' + xmlfile, output_to=utftempxmlfile, errors_to='log/iconv.log', stderr_check=1),
                                                                          Command('xmllint --encode UTF-8 ' + utftempxmlfile, output_to=utfxmlfile, errors_to='log/xmllint.log', stderr_check=1)])
                # Everybody gets xml tidied before processing further
                self.targets.add(tidyxmlfile,    [utfxmlfile],           [Command('tidy -config /etc/lampadas/tidyrc -quiet ' + utfxmlfile, output_to=tidyxmlfile, errors_to='log/tidy.log', stderr_check=1)])

                # Now we have good DocBook XML, generate all outputs
                self.targets.add(htmlfile,       [tidyxmlfile],          [Command('xsltproc --param quiet 1 --maxdepth 100 ' + XSLTPROC_PARAMS + ' ' + config.xslt_html + ' ' + tidyxmlfile, output_to=htmlfile, errors_to='log/xsltproc.log', stderr_check=1)])
                self.targets.add(indexfile,      [tidyxmlfile],          [Command('xsltproc --param quiet 1 --maxdepth 100 ' + XSLTPROC_PARAMS + ' ' + config.xslt_chunk + ' ' + tidyxmlfile)])
                self.targets.add(omffile,        [tidyxmlfile],          [Command(config.db2omf + ' ' + tidyxmlfile + ' -o ' + omffile, errors_to='log/db2omf.log', stderr_check=1)])
                self.targets.add(txtfile,        [htmlfile],             [Command('lynx --dump --nolist ' + htmlfile, output_to=txtfile, errors_to='log/lynx.log', stderr_check=1)])

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
        
        If the document not been mirrored, this routine will not
        attempt to build it.

        If the document already has make errors against it, they
        will be cleared before the make is attempted.
        """

        # Do not publish any document which has not been mirrored.
        if self.doc.mirror_time=='':
            return

        # Clear any make errors.
        self.doc.errors.clear('make')

        # Build the requested target.
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

        # All dependencies are built, so now this target
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
        #log(3, 'Checking target: ' + name + ', timestamp: ' + str(timestamp) + ', high_timestamp: ' + str(high_timestamp))
        if timestamp <= high_timestamp:
            timestamp = time.time()

            # If there is no target, the alleged target is a leaf point.
            if not target==None:

                for key in target.commands.sort_by('sort_order'):
                    command = target.commands[key]
                    
                    # Go to the work directory
                    cmd_text = 'cd ' + self.workdir + '; '

                    # Erase the error log if it exists
                    if command.errors_to > '':
                        cmd_text += ' rm -f ' + command.errors_to + '; '

                    # Run he command, piping output and errors appropriately
                    cmd_text = cmd_text + command.command
                    if command.output_to > '':
                        cmd_text += ' > ' + command.output_to
                    if command.errors_to > '':
                        cmd_text += ' 2>>' + command.errors_to
                        
                    log(3, 'Running: ' + cmd_text)
                    exit_status = os.system(cmd_text)

                    # Abort if the command returns an exit code.
                    if exit_status<>0:
                        self.doc.errors.add(ERR_MAKE_EXIT_STATUS, str(exit_status) + ': ' + cmd_text)
                        log(0, 'ERROR: The command returned error code ' + str(exit_status) + '.')
                    
                    # Abort if there is anything written to STDERR.
                    if command.stderr_check==1 and  command.errors_to > '':
                        fh = open(self.workdir + command.errors_to, 'r')
                        err_text = fh.read()
                        fh.close()
                        if err_text > '':
                            self.doc.errors.add(ERR_MAKE_STDERR, cmd_text + '\n\n' + err_text)
                            log(0, 'ERROR: The command wrote to STDERR.')
                            if exit_status==0:
                                exit_status = 1;
                            
                    # Zero filesize indicates failure. Fail and erase file.
                    filestat = os.stat(self.workdir + command.output_to)
                    filesize = filestat[stat.ST_SIZE]
                    if filesize==0:
                        self.doc.errors.add(ERR_MAKE_ZERO_LENGTH, cmd_text)
                        log(0, 'ERROR: The command left a zero-length file. Removing.')
                        if exit_status==0:
                            exit_status = 2;

                    if exit_status <> 0:
                        if command.output_to > '':
                            os.remove(self.workdir + command.output_to)
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
        
        # Do not publish any document which has not been mirrored.
        if self.doc.mirror_time=='':
            return

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
    config.log_level = 3
    config.log_console = 1
    config.log_sql = 0
    projects.write()
    projects.write_main()

    # Read the command line for a requested target
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            print 'Making target ' + arg + '...'
            projects.write()
            projects.make(arg)
    else:
        projects.write()
        projects.make()

