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

from globals import *
from Config import config
from mod_python import apache
from Lintadas import lintadas
from Mirror import mirror
import os

from CoreDM import dms

def show_config(req):
    return error(config.debug())

def run_lintadas(req, doc_id):
    doc = dms.document.get_by_id(int(doc_id))
    if doc==None:
        return error("Cannot find document " + doc_id)

    lintadas.check_doc(doc.id)
    lintadas.check_files(doc.id)
    go_back(req)

def run_mirror(req, doc_id):
    doc = dms.document.get_by_id(int(doc_id))
    if doc==None:
        return error("Cannot find document " + str(doc_id))

    if doc.lint_time=='':
        lintadas.check_doc(doc.id)
        lintadas.check_files(doc.id)
    if doc.lint_time=='':
        return error("Error inspecting document " + doc_id)
        
    mirror.mirror(doc.id)
    if doc.mirror_time=='':
        return error("Error mirroring document " + doc_id)
    go_back(req)

def run_publish(req, doc_id):
    doc = dms.document.get_by_id(int(doc_id))
    if doc==None:
        return error("Cannot find document " + doc_id)

    if doc.lint_time=='':
        lintadas.check_doc(doc.id)
        lintadas.check_files(doc.id)
    if doc.lint_time=='':
        return error("Error inspecting document " + doc_id)
        
    if doc.mirror_time=='':
        mirror.mirror(doc.id)
    if doc.mirror_time=='':
        return error("Error mirroring document " + doc_id)
    
    # Instantiate and run the Makefile.py project.
    from Makefile import Project
    project = Project(doc.id)
    
    project.write()
    project.make('clean')
    project.make('publish')
    go_back(req)

