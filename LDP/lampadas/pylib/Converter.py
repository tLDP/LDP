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

	def ConvertSGMLFile(self, filename, format):
		if format == 'XML' or format == 'SGML':
			command = 'xsltproc '
			if format == 'SGML':
				command = command + '--docbook '
			command = command + '/usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/docbook.xsl ' + filename
			result = commands.getoutput(command)
		else:
			return "FORMAT NOT YET SUPPORTED"
		return result


#if __name__ == "__main__":
