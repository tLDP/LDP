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
This module subclasses the Document class to generate an OMF structure for it.
"""

# Modules

from Globals import *
from Config import config
from DataLayer import lampadas, User
from WebLayer import lampadasweb    # FIXME: Obviously strings are not just used
                                    # for the web! Move them out of WebLayer.

class OMF:

    def __init__(self, doc_id):
        self.id = doc_id
        self.doc = lampadas.docs[doc_id]
        omf = WOStringIO('<resource id="%s">\n'
                         '%s'
                         '%s'
                         '%s'
                         '<title>%s</title>\n'
                         '<date>%s</date>\n'
                         '<versiongroup>\n'
                         '  <version>\n'
                         '    <id>%s</id>\n'
                         '    <date>%s</date>\n'
                         '  </version>\n'
                         '</versiongroup>\n'
                         '<type>%s</type>\n'
                         '%s\n'
                         '<identifier>%s</identifier>\n'
                         '%s'
                         '<source>%s (%s)</source>\n'
                         '<language>%s</language>\n'
                         '%s'
                         '</resource>\n'
                         % (self.id,
                            self.creators(),
                            self.maintainers(),
                            self.contributors(),
                            self.doc.title,
                            self.doc.pub_date,
                            self.doc.version,
                            self.doc.pub_date,
                            self.doc.type_code,
                            self.format(),
                            self.doc.sk_seriesid,
                            self.description(),
                            config.hostname, config.project_name,
                            self.doc.lang,
                            self.rights(),
                           ))
        self.omf = omf.get_value()

    def creators(self):
        omf = WOStringIO()
        for key in self.doc.users.keys():
            docuser = self.doc.users[key]
            user = User(docuser.username)
            if docuser.role_code=='author':
                omf.write('<creator>%s' % user.email)
                if user.name > '':
                    omf.write(' (%s)' % user.name)
                omf.write('</creator>\n')
        return omf.get_value()

    def maintainers(self):
        omf = WOStringIO()
        for key in self.doc.users.keys():
            docuser = self.doc.users[key]
            user = User(docuser.username)
            if docuser.role_code=='maintainer':
                omf.write('<maintainer>%s' % user.email)
                if user.name > '':
                    omf.write(' (%s)' % user.name)
                omf.write('</maintainer>\n')
        return omf.get_value()

    def contributors(self):
        omf = WOStringIO()
        for key in self.doc.users.keys():
            docuser = self.doc.users[key]
            user = User(docuser.username)
            if docuser.role_code <> 'author' and docuser.role_code <> 'maintainer':
                omf.write('<contributor>%s' % user.email)
                if user.name > '':
                    omf.write(' (%s)' % user.name)
                omf.write('</contributor>\n')
        return omf.get_value()

    def format(self):
        omf = WOStringIO()
        if self.doc.format_code=='xml':
            omf.write('<format dtd="%s" mime="text/xml"/>' % self.doc.dtd_code)
        elif self.doc.format_code=='sgml':
            if self.doc.dtd_code=='html':
                omf.write('<format dtd="%s" mime="text/html"/>' % self.doc.dtd_code)
            else:
                omf.write('<format dtd="%s" mime="text/sgml"/>' % self.doc.dtd_code)
        elif self.doc.format_code=='text':
            omf.write('<format mime="text/plain"/>')
        elif self.doc.format_code=='latex':
            omf.write('<format mime="application/x-latex"/>')
        return omf.get_value()

    def description(self):
        if self.doc.abstract > '':
            return '<description>%s</description>' % self.doc.abstract
        else:
            return ''

    def rights(self):
        if self.doc.license_code=='':
            return ''
        license = lampadas.licenses[self.doc.license_code]
        if license.url=='':
            return '<rights><type>%s</type></rights>\n' % license.code
        else:
            return '<rights><type>%s</type><license>%s</license></rights>\n' % (license.code, license.url)


if __name__=='__main__':
    print '<xml version="1.0" encoding="UTF-8"?>'
    print '<omf>'
    for doc_id in lampadas.docs.sort_by('id'):
        print OMF(doc_id).omf
    print '</omf>'

