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
Lampadas Conversion Module

NOTE: This module is obsolete. When I realized every conversion
was a call to an external program, I began writing a Makefile for
each document during the mirroring process.

This module converts source documents into DocBook XML format.

Currently supported source formats are:

	Plain Text
	WikiText
	Texinfo
	DocBook SGML
	Linuxdoc

Working on:

Pie-in-the-sky:

	DebianDoc
	PyDoc
	*roff
"""

# Modules ##################################################################

from Log import log
import commands


# Constants


# Globals


# Converter

class Converter:

	def text(self, Filename, Format):
		log(3, 'Converting ' + Filename + ' from text')
		return wikitext(Filename)

	def wikitext(self, Filename):
		log(3, 'Converting ' + Filename + ' from WikiText')
		command = 'wt2db -x ' + Filename
		result = commands.getoutput(command)
		return result

	def texinfo(self, Filename):
		log(3, 'Converting ' + Filename + ' from Texinfo')
		command = 'texi2db -f ' + Filename
		result = commands.getoutput(command)
		return result

	def ldsgml(self, Filename):
		log(3, 'Converting ' + Filename + ' from LinuxDoc SGML')
		command = ''
		result = commands.getoutput(command)
		return result

	def dbsgml(self, Filename):
		log(3, 'Converting ' + Filename + ' from DocBook SGML')
		command = 'xmllint --sgml ' + Filename
		result = commands.getoutput(command)
		return result


def main():

	C = Converter()
#	output = C.texinfo('test/texinfo/texinfo.txi')
	output = C.dbsgml('test/db3.0sgml/RPM-HOWTO.sgml')
	print output

if __name__ == "__main__":
	main()
