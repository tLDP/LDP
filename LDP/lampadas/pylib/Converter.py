#!/usr/bin/python

"""
Lampadas Conversion Module

This module converts source documents into DocBook XML format.

Currently supported source formats are:

	Plain Text
	WikiText
	Texinfo
	DocBook SGML

Working on:

	Linuxdoc
	DebianDoc
"""

# Modules ##################################################################

from Log import Log
import commands


# Constants


# Globals

Log = Log()


# Converter

class Converter:

	def text(self, Filename, Format):
		Log(3, 'Converting ' + Filename + ' from text')
		return WikiText(Filename)

	def wikitext(self, Filename):
		Log(3, 'Converting ' + Filename + ' from WikiText')
		command = 'wt2db -x ' + Filename
		result = commands.getoutput(command)
		return result

	def texinfo(self, Filename):
		Log(3, 'Converting ' + Filename + ' from Texinfo')
		command = 'texi2db -f ' + Filename
		result = commands.getoutput(command)
		return result

	def dbsgml(self, Filename):
		Log(3, 'Converting ' + Filename + ' from DocBook SGML')
		command = 'xmllint --sgml ' + Filename
		result = commands.getoutput(command)
		return result

	def ldsgml(self, Filename):
		Log(3, 'Converting ' + Filename + ' from LinuxDoc SGML')
		command = ''
		result = commands.getoutput(command)
		return result


	def xml(self, Filename):
		command = 'xsltproc /usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/docbook.xsl ' + Filename
		result = commands.getoutput(command)
		return result

	def sgml(self, Filename, Format):
		command = 'xsltproc --docbook /usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/docbook.xsl ' + Filename
		result = commands.getoutput(command)
		return result


if __name__ == "__main__":
	C = Converter()
#	output = C.texinfo('test/texinfo/texinfo.txi')
	output = C.dbsgml('test/db3.0sgml/RPM-HOWTO.sgml')
	print output
