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

from Globals import *
from globals import *
from Config import config
from DataLayer import lampadas
from WebLayer import lampadasweb
from HTML import page_factory
from URLParse import URI
from Log import log
from mod_python import apache
import os

def document(req, title='',
                  pub_status_code='',
                  type_code='',
                  subtopic_code='',
                  maintained='',
                  maintainer_wanted=''):
    """
    Returns the results of a document search.
    """
    
    # Replace null strings with None
    search_title             = None
    search_pub_status_code   = None
    search_type_code         = None
    search_subtopic_code     = None
    search_maintained        = None
    search_maintainer_wanted = None
    if title > '':
        search_title = title
    if pub_status_code > '':
        search_pub_status_code = pub_status_code
    if type_code > '':
        search_type_code = type_code
    if subtopic_code > '':
        search_subtopic_code = subtopic_code
    if maintained > '':
        message = 'maintained is ' + maintained
        search_maintained = int(maintained)
    if maintainer_wanted > '':
        search_maintainer_wanted = int(maintainer_wanted)
    
    uri = URI(req.uri)
    page = lampadasweb.pages['doctable']

    # This avoids the use of a copy.deepcopy().
    save_page = page.page[uri.lang]
    table = page_factory.tablef.doctable(uri, None, title=search_title,
                                                    pub_status_code=search_pub_status_code,
                                                    type_code=search_type_code,
                                                    subtopic_code=search_subtopic_code,
                                                    maintained=search_maintained,
                                                    maintainer_wanted=search_maintainer_wanted)
    page.page[uri.lang] = page.page[uri.lang].replace('|tabdocs|', table)
    html = page_factory.build_page(page, URI('doctable' + uri.lang_ext), None)
    
    page.page[uri.lang] = save_page
    return html

