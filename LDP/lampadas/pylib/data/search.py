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
from Tables import tables
from Sessions import sessions
from URLParse import URI
from Log import log
from mod_python import apache
import os

def document(req,
             title='',
             pub_status_code='',
             type_code='',
             subtopic_code='',
             maintained='',
             maintainer_wanted='',
             lang='',
             review_status_code='',
             tech_review_status_code='',
             pub_date='',
             last_update='',
             tickle_date='',
             isbn='',
             rating='',
             format_code='',
             dtd_code='',
             license_code='',
             copyright_holder='',
             sk_seriesid='',
             abstract='',
             short_desc=''
             ):
    """
    Returns the results of a document search.
    """

    # Read session state
    sessions.get_session(req)

    uri = URI(req.uri)
    page = lampadasweb.pages['doctable']

    # serve search results by manually replacing the
    # doctable here instead of during the regular call.
    # It's a bit ugly, but works.

    # We store and restore the contents to avoid doing
    # a copy.deepcopy() which I haven't tested but imagine to
    # be rather expensive. -- DCM
    save_page = page.page[uri.lang]
    table = tables.doctable(uri, 
                            title                   = empty2None_str(title),
                            pub_status_code         = empty2None_str(pub_status_code),
                            type_code               = empty2None_str(type_code),
                            subtopic_code           = empty2None_str(subtopic_code),
                            maintained              = empty2None_int(maintained),
                            maintainer_wanted       = empty2None_int(maintainer_wanted),
                            lang                    = empty2None_str(lang),
                            review_status_code      = empty2None_str(review_status_code),
                            tech_review_status_code = empty2None_str(tech_review_status_code),
                            pub_date                = empty2None_str(pub_date),
                            last_update             = empty2None_str(last_update),
                            tickle_date             = empty2None_str(tickle_date),
                            isbn                    = empty2None_str(isbn),
                            rating                  = empty2None_str(rating),
                            format_code             = empty2None_str(format_code),
                            dtd_code                = empty2None_str(dtd_code),
                            license_code            = empty2None_str(license_code),
                            copyright_holder        = empty2None_str(copyright_holder),
                            sk_seriesid             = empty2None_str(sk_seriesid),
                            abstract            = empty2None_str(abstract),
                            short_desc          = empty2None_str(short_desc))

    page.page[uri.lang] = page.page[uri.lang].replace('|tabdocs|', table)
    uri = URI('doctable' + uri.lang_ext)
    uri.base = '../../'
    html = page_factory.build_page(page, uri)
    
    # Restore the original page
    page.page[uri.lang] = save_page
    return html

def empty2None_str(astring):
    if astring=='':
        return None
    return astring

def empty2None_int(astring):
    if astring=='':
        return None
    return int(astring)

