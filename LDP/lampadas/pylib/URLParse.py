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
The API is documented in the Lampadas Programmer's Guide. A summary:

[Language/][doc/<ID>[/<format>]|author/<ID>|$topic/$class]
"""

import string
from DataLayer import lampadas

def splitterm(term, sep):
    """
    Splits the term into 2 pieces according to the seperator,
    and returns them. If the term does not contain the sep,
    the second string the returned tuple wil be ''.
    """

    temp = string.split(term, sep, 1)
    if len(temp) > 1:
        return temp[0], temp[1]
    else:
        return temp[0], ''
    

class URI:

    def __init__(self, uri):
    
        self.protocol = ""
        self.server = ""
        self.port = ""
        self.language = "EN"
        self.force_lang = 0
        self.path = ""
        self.service = ""
        self.format = ""
        self.filename = "home"
        self.id = 0
        self.parameter = ""
        self.anchor = ""

        self.uri = uri
        
        temp = uri
        if len(temp) == 0:
            return
        if temp[0] == '/':
            temp = temp[1:]
        
        if len(temp) == 0:
            return
        if temp[-1] == '/':
            temp = temp[:-1]

        if temp.find('://') > 0:
            self.protocol, temp = splitterm(temp, '://')
            self.server, temp = splitterm(temp,'/')
            if self.server.find(':') > 0:
                self.server, self.port = splitterm(self.server, ':')
        if temp.find('#') > 0:
            temp, self.anchor = splitterm(temp, '#')
        if temp.find('?') > 0:
            temp, self.parameter = splitterm(temp, '?')
        
        temp = string.split(temp, '/')

        if len(temp) > 0:
            lang = lampadas.Languages[temp[0]]
            if not lang == None:
                self.language = temp[0]
                temp = temp[1:]
                self.force_lang = 1

        if len(temp) > 0:
            if temp[0] == 'doc' or temp[0] == 'editdoc':
            # FIXME:
            # 
            # This really should eb using only a single attribute, 'Filename'.
            # The 'doc' kludge should use a regular page which then embeds document
            # content.
                if temp[0] == 'doc':
                    self.service = temp[0]
                    self.filename = ''
                else:
                    self.service = ''
                    self.filename = temp[0]
                temp = temp[1:]
                if len(temp) > 0:
                    self.id = int(temp[0])
                    temp = temp[1:]
                    if len(temp) > 0:
                        if temp[0] == 'xml' or temp[0] == 'html' or temp[0] == 'omf':
                            self.format = temp[0]
                        else:
                            self.filename = temp[0]
            else:
                if len(temp) == 1:
                    self.path = '/'
                    if len(temp[0]) > 0:
                        self.filename = temp[0]
                else:
                    self.path = string.join(temp[:-1], '/')
                    if len(temp[-1]) > 0:
                        self.filename = temp[-1]


    def printdebug(self):
        print "URI: [" + self.uri + "]"
        print "Protocol: [" + self.protocol + "]"
        print "Server: [" + self.server + "]"
        print "Port: [" + self.port + "]"
        print "Path: [" + self.path + "]"
        print "Language: [" + self.language + "]"
        print "Forced Language: [" + str(self.force_lang) + "]"
        print "Service: [" + self.service+ "]"
        print "ID [" + str(self.id) + "]"
        print "Format [" + str(self.format) + "]"
        print "Filename: [" + self.filename + "]"
        print "Parameter: [" + self.parameter + "]"
        print "Anchor: [" + self.anchor + "]"


if __name__ == '__main__':
    import sys

    foo = URI(sys.argv[1])
    #'http://localhost:8000/EN/editdoc/1/home?docid=1#foo')
    foo.printdebug()
