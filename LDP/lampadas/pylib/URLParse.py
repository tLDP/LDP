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
The URLParse module deciphers a Lampadas URL into its component parts.
The API is documented in the Lampadas Programmer's Guide.
"""

#from WebLayer import lampadasweb

from Log import log
import urlparse
import os
import string

from Globals import WOStringIO
from CoreDM import dms

# Only load this once. No need to support adding languages during runtime!
AVAILABLE_LANG = dms.language.get_all().keys('code')

class URI:
    """
    FIXME: explain what the different attributes are used for.
    """
    
    def __init__(self, uri):

        log(3, "parsing URI: " + uri)
        self.protocol = ""
        self.server = ""
        self.port = ""
        self.lang = "EN"
        self.lang_ext = '.html'
        self.path = "/"
        self.parameter = ""
        self.anchor = ""

        self.page_code = ''
        self.page_data = ''

        # If the URL specifies a user, doc, etc., it is stored in one
        # of these attributes.
        self.username = ''
        self.filename = ''
        self.code = ''
        self.id = 0
        self.code = ''
        self.letter = ''

        # Any of the above is duplicated here as a string.
        # Ugly, but this way we can read data easily
        # w/o caring what type might be there.
        self.data = []

        if uri > '' and uri[0]=='/':
            self.uri = uri[1:]
        else:
            self.uri = uri

        self.base = ''
        for i in range(self.uri.count('/')):
            self.base += '../'
        
        protocol, host, path, params, query, fragment = urlparse.urlparse(uri)

        # protocol, server, port, anchor, parameters
        self.protocol = protocol
        if host.find(':') > 0 :
            self.server, self.port = host.split(':')
        else :
            self.server = host
        self.parameter = query
        self.anchor = fragment
       
        # Default page if none was passed, is index
        if path in ('', '/'):
            path='index.html'

        # Discard initial and terminal /
        if len(path) > 0:
            if path[-1]=='/':
                path = path[:-1]
        if len(path) > 0:
            if path[0]=='/':
                path = path[1:]

        # Discard .html extension
        if len(path) > 5:
            if path[-5:]=='.html':
                path = path[:-5]
       
        # Locate language extension
        if len(path) > 3:
            if path[-3]=='.':
                lang = path[-2:]
                if lang.upper() in AVAILABLE_LANG:
                    self.lang = lang.upper()
                    self.lang_ext = '.' + lang.lower() + '.html'
                    path = path[:-3]
                else:
                    self.lang_ext = '.' + 'en.html'
            else:
                self.lang_ext = '.' + 'en.html'

        # Split up the path
        if path.count('/')==0:
            self.page_code = path
        else:
            data = path.split('/')
            self.page_code = data[0]
            self.data = data[1:]

        page = dms.page.get_by_id(self.page_code)
        if page==None:
            print "ERROR: page not found."
            self.print_debug()
            return
        
        # If the page specifies that it includes an object,
        # read the identifier for the object.

        # FIXME: As a temporary fix, we reload any embedded data, to overcome
        # the shortcomings of the caching system. We really need to just
        # fix the cache, but this is a quick fix for now.
        self.page_data = page.data
        data = self.data
        for item in page.data:
            if len(data)==0:
                break
            if item in ('doc', 'news'):
                self.id = int(data[0])
                data = data[1:]
            elif item in ('collection', 'topic', 'type', 'report', 'page', 'string'):
                self.code = data[0]
                data = data[1:]
            elif item in ('user',):
                self.username = data[0]
                data = data[1:]
            elif item in ('letter',):
                self.letter = data[0]
                data = data[1:]
            elif item in ('filename',):
                self.filename = string.join(data, '/')
                break

    def print_debug(self):
        print self.debug_info()

    def debug_info(self):
        info = WOStringIO()
        info.write("URI: [%s]\n"                % self.uri)
        info.write("Base: [%s]\n"               % self.base)
        info.write("Protocol: [%s]\n"           % self.protocol)
        info.write("Server: [%s]\n"             % self.server)
        info.write("Port: [%s]\n"               % self.port)
        info.write("Path: [%s]\n"               % self.path)
        info.write("Page Code: [%s]\n"          % self.page_code)
        info.write("Page Data: [%s]\n"          % self.page_data)
        info.write("Language: [%s]\n"           % self.lang)
        info.write("Language Extension: [%s]\n" % self.lang_ext)
        info.write("Parameter: [%s]\n"          % self.parameter)
        info.write("Anchor: [%s]\n"             % self.anchor)
        info.write("ID: [%s]\n"                 % self.id)
        info.write("Code [%s]\n"                % self.code)
        info.write("Letter: [%s]\n"             % self.letter)
        info.write("Username: [%s]\n"           % self.username)
        info.write("Filename: [%s]\n"           % self.filename)
        info.write("Data: [%s]\n"               % self.data)
        return info.get_value()


if __name__=='__main__':
    import sys

    foo = URI(sys.argv[1])
    foo.print_debug()
