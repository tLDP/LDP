#!/usr/bin/python

"""
Lampadas Conversion Module

This module converts source documents into DocBook XML format.

Currently supported source formats are:

	Plain Text
	WikiText
	Texinfo

Working on:

	DocBook SGML

For 1.0:

	Linuxdoc

For 1.0+:

	DebianDoc
	HTML
"""

# Modules ##################################################################

from Log import Log
import commands


# Constants


# Globals

Log = Log()


# Converter

class Converter:

	def Text(self, Filename, Format):
		Log(3, 'Converting ' + Filename + ' from text')
		return WikiText(Filename)

	def WikiText(self, Filename):
		Log(3, 'Converting ' + Filename + ' from WikiText')
		command = 'wt2db -a ' + Filename
		result = commands.getoutput(command)
		return result

	def Texinfo(self, Filename):
		Log(3, 'Converting ' + Filename + ' from Texinfo')
		command = 'texi2db -f ' + Filename
		result = commands.getoutput(command)
		return result

	def DBSGML(self, Filename):
		Log(3, 'Converting ' + Filename + ' from DocBook SGML')
		command = ''
		result = commands.getoutput(command)
		return result

	def LinuxDoc(self, Filename):
		Log(3, 'Converting ' + Filename + ' from LinuxDoc SGML')
		command = ''
		result = commands.getoutput(command)
		return result


	def XML(self, Filename):
		command = 'xsltproc /usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/docbook.xsl ' + Filename
		result = commands.getoutput(command)
		return result

	def SGML(self, Filename, Format):
		command = 'xsltproc --docbook /usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/docbook.xsl ' + Filename
		result = commands.getoutput(command)
		return result


if __name__ == "__main__":
	C = Converter()
	output = C.Texinfo('test/texinfo/texinfo.txi')
	print output
