#!/usr/bin/python

"""
Lampadas Conversion Module

This module converts source documents into DocBook XML format.
"""

# Modules ##################################################################

import commands


# Constants


# Globals


# Converter

class Converter:

	def ConvertSGMLFile(self, Filename, Format):
		if Format == 'XML' or Format == 'SGML':
			command = 'xsltproc '
			if Format == 'SGML':
				command = command + '--docbook '
			command = command + '/usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/docbook.xsl ' + Filename
			result = commands.getoutput(command)
		else:
			return 'FORMAT ' + Format + ' NOT YET SUPPORTED'
		return result


#if __name__ == "__main__":
