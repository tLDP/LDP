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

from DataLayer import lampadas
from WebLayer import lampadasweb
from Log import log
import urlparse
import os

AVAILABLE_LANG = lampadas.languages.keys()
#AVAILABLE_LANG = ['FR','EN','ES']
#def log(a,b): pass

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

        self.force_lang = 0
              
        self.filename = "home"

        # If the URL specifies a user, doc, etc., it is stored in one
        # of these attributes.
        self.username = ''
        self.id = 0
        self.code = ''
        self.letter = ''

        # Any of the above is duplicated here as a string.
        # Ugly, but this way we can read data easily
        # w/o caring what type might be there.
        self.data = ''

        self.uri = uri
        self.base = uri
        
        protocol, host, path, params, query, fragment = urlparse.urlparse(uri)

        # protocol, server, port, anchor, parameters
        self.protocol = protocol
        if host.find(':') > 0 :
            self.server, self.port = host.split(':')
        else :
            self.server = host
        self.parameter = query
        self.anchor = fragment
       
        # Default page if none was passed, is home
        if path in ('', '/'):
            path='home.html'

        # Discard initial /
        if len(path) > 0:
            if path[-1]=='/':
                path = path[:-1]

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

        # Split the path
        self.filename, self.data = os.path.split(path)
        
        # If there was no data, move data into filename
        if self.filename in ('', '/'):
            self.filename = self.data
            self.data = ''
        else:
            self.path, self.filename = os.path.split(self.filename)

        # Discard initial /
        if len(self.filename) > 0:
            if self.filename[0]=='/':
                self.filename = self.filename[1:]

        page = lampadasweb.pages[self.filename]
        if page==None:
            self.printdebug()
            
        if page.data in ('doc',):
            self.id = int(self.data)
        elif page.data in ('topic', 'subtopic', 'type'):
            self.code = self.data
        elif page.data in ('user',):
            self.username = self.data
        elif page.data in ('letter',):
            self.letter = self.data

    def printdebug(self):
        print "URI: [%s]"                % self.uri
        print "Base: [%s]"               % self.base
        print "Protocol: [%s]"           % self.protocol
        print "Server: [%s]"             % self.server
        print "Port: [%s]"               % self.port
        print "Path: [%s]"               % self.path
        print "Filename: [%s]"           % self.filename
        print "Language: [%s]"           % self.lang
        print "Language Extension: [%s]" % self.lang_ext
        print "Parameter: [%s]"          % self.parameter
        print "Anchor: [%s]"             % self.anchor
        print "ID: [%s]"                 % self.id
        print "Code [%s]"                % self.code
        print "Letter: [%s]"             % self.letter
        print "Data: [%s]"               % self.data


if __name__=='__main__':
    import sys

    foo = URI(sys.argv[1])
    #foo = URI('http://localhost:8000/EN/editdoc/1/home?docid=1#foo')
    foo.printdebug()
