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
Lampadas Error Checking Module

This module performs all kinds of automatic checks on data in the database
and the source files it points to. Errors are logged in the
document_error table.
"""

# Modules ##################################################################

from Config import config
from Log import log
from DataLayer import lampadas
import os


# Constants


# Globals


# Lintadas

class Lintadas:

	def CheckAllDocs(self):
		keys = lampadas.Docs.keys()
		for key in keys:
			self.CheckDoc(key)
	
	def CheckDoc(self, DocID):
		log(3, 'Running Lintadas on document ' + str(DocID))
		Doc = lampadas.Docs[int(DocID)]
		assert not Doc == None
		Doc.Errs.Clear()

		# Test document files
		keys = Doc.Files.keys()
		for key in keys:

			File = Doc.Files[key]

			if File.IsLocal:
				log(3, 'Checking filename ' + key)
			else:
				log(3, 'Skipping remote file ' + key)
				continue

			# Determine file format
			self.filename = File.Filename.upper()
			if self.filename[-5:] == '.SGML':
				FileFormat = "SGML"
				DocFormat = 'SGML'
			elif self.filename[-4:] == '.XML':
				FileFormat = "XML"
				DocFormat = 'XML'
			elif self.filename[-3:] == '.WT':
				FileFormat = 'WIKI'
				DocFormat = 'WIKI'
			else:
				FileFormat = ''
				DocFormat = ''

			formatkeys = lampadas.Formats.keys()
			for formatkey in formatkeys:
				if lampadas.Formats[formatkey].I18n['EN'].Name == FileFormat:
					File.FormatID = formatkey
				if lampadas.Formats[formatkey].I18n['EN'].Name == DocFormat:
					Doc.FormatID = formatkey
			
			log(3, 'file format is ' + FileFormat)
			
			# Determine DTD for SGML and XML files
			if FileFormat == 'XML' or FileFormat == 'SGML':
				DTDVersion = ''
				try:
					command = 'grep -i DOCTYPE ' + config.cvs_root + File.Filename + ' | head -n 1'
					grep = os.popen(command, 'r')
					DTDVersion = grep.read()
				except IOError:
					pass

				DTDVersion = DTDVersion.upper()
				if DTDVersion.count('DOCBOOK') > 0:
					Doc.DTD = 'DocBook'
				elif DTDVersion.count('LINUXDOC') > 0:
					Doc.DTD = 'LinuxDoc'
				else:
					Doc.DTD = ''

			log(3, 'doc dtd is ' + Doc.DTD)

			Doc.Save()
			File.Save()
		log(3, 'Lintadas run on document ' + str(DocID) + ' complete')

lintadas = Lintadas()

# When run at the command line, check the document requested.
# If no document was specified, all checks are performed on all documents.
# 

def main():
	import getopt
	import sys

	Docs = sys.argv[1:]
	if len(Docs) == 0:
		print "Running on all documents..."
		lintadas.CheckAllDocs()
	else:
		for Doc in Docs:
			lintadas.CheckDoc(Doc)

def usage():
	print "Lintadas version " + VERSION
	print
	print "This is part of the Lampadas System"
	print
	print "Pass doc ids to run Lintadas on specific docs,"
	print "or call with no parameters to run Lintadas on all docs."
	print


if __name__ == "__main__":
	main()
