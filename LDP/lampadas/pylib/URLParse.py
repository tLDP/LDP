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
from Log import log
import urlparse

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
        self.force_lang = 0
        self.path = "/"
        self.format = ""
        self.filename = "home"
        self.id = 0
        self.code = ''
        self.parameter = ""
        self.anchor = ""

        self.uri = uri
        
        protocol, host, path, params, query, fragment = urlparse.urlparse(uri)

        # protocol, server, port, anchor, parameters
        self.protocol = protocol
        if host.find(':') > 0 :
            self.server, self.port = host.split(':')
        else :
            self.server = host
        self.parameter = query
        self.anchor = fragment
        
        # path
        self.base = path
        path = path.split('/')

        if not path : return
        if path[0] == '' :
            path = path[1:]

        if not path : return
        if path[-1] == '' :
            path = path[:-1]

        if not path : return
        if path[0] in AVAILABLE_LANG :
            self.force_lang = 1
            self.lang, path = path[0], path[1:]
            self.base = '/'.join(path)

        # this is where we load ids and codes for pages which
        # contain an object and display its attributes.
        if not path : return
        if path[0] in ('editdoc','cvslog'):
            self.filename = path[0]
            path = path[1:]
            if path :
                self.id = int(path[0])
        elif path[0] in ('topic','subtopic','type'):
            self.filename = path[0]
            path = path[1:]
            if path :
                self.code = path[0]
        elif path[0] in ('user',):
            self.filename = path[0]
            path = path[1:]
            if path :
                self.username = path[0]
        else:
            if len(path)==1:
                self.path = '/'
                if len(path[0]) > 0:
                    self.filename = path[0]
            else:
                self.path = '/'.join(path[:-1])
                if len(path[-1]) > 0:
                    self.filename = path[-1]

    def printdebug(self):
        print "URI: [%s]"      % self.uri
        print "Base: [%s]"     % self.base
        print "Protocol: [%s]" % self.protocol
        print "Server: [%s]"   % self.server
        print "Port: [%s]"     % self.port
        print "Path: [%s]"     % self.path
        print "Language: [%s]" % self.lang
        print "Forced Language: [%s]" % self.force_lang
        print "ID: [%s]"       % self.id
        print "Code [%s]"      % self.code
        print "Format [%s]"    % self.format
        print "Filename: [%s]" % self.filename
        print "Parameter: [%s]"% self.parameter
        print "Anchor: [%s]"   % self.anchor


if __name__=='__main__':
    import sys

    foo = URI(sys.argv[1])
    #foo = URI('http://localhost:8000/EN/editdoc/1/home?docid=1#foo')
    foo.printdebug()
