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
from Sessions import sessions
from URLParse import URI
from Log import log
from mod_python import apache
import os

def document(req, title='',
                  pub_status_code='',
                  type_code='',
                  subtopic_code='',
                  maintained='',
                  maintainer_wanted='',
                  lang=''):
    """
    Returns the results of a document search.
    """

    # Read session state
    sessions.get_session(req)

    # Replace null strings with None
    search_title             = None
    if title > '':
        search_title = title
    search_pub_status_code   = None
    if pub_status_code > '':
        search_pub_status_code = pub_status_code
    search_type_code         = None
    if type_code > '':
        search_type_code = type_code
    search_subtopic_code     = None
    if subtopic_code > '':
        search_subtopic_code = subtopic_code
    search_maintained        = None
    if maintained > '':
        search_maintained = int(maintained)
    search_maintainer_wanted = None
    if maintainer_wanted > '':
        search_maintainer_wanted = int(maintainer_wanted)
    search_lang = None
    if lang > '':
        search_lang = lang
    
    uri = URI(req.uri)
    page = lampadasweb.pages['doctable']

    # serve search results by manually replacing the
    # doctable here instead of during the regular call.
    # It's a bit ugly, but works.

    # We store and restore the contents to avoid doing
    # a copy.deepcopy() which I haven't tested but imagine to
    # be rather expensive. -- DCM
    save_page = page.page[uri.lang]
    table = page_factory.tablef.doctable(uri, title=search_title,
                                              pub_status_code=search_pub_status_code,
                                              type_code=search_type_code,
                                              subtopic_code=search_subtopic_code,
                                              maintained=search_maintained,
                                              maintainer_wanted=search_maintainer_wanted,
                                              lang=search_lang)
    page.page[uri.lang] = page.page[uri.lang].replace('|tabdocs|', table)
    html = page_factory.build_page(page, URI('doctable' + uri.lang_ext))
    
    # Restore the original page
    page.page[uri.lang] = save_page
    return html

