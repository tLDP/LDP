#!/usr/bin/python

"""
Lampadas Error Checking Module

This module performs all kinds of automatic checks on data in the database
and the source files it points to. Errors are logged in the
document_error table.
"""

# Modules ##################################################################

import DataLayer
import Log
import os

# Constants


# Globals

L = DataLayer.Lampadas()
Log = Log.Log()
cvs_root = L.Config('cvs_root')


# Lintadas

class Lintadas:

	def __call__(self, DocID):
		self.CheckDoc(DocID)

	def CheckAllDocs(self):
		keys = L.Docs.keys()
		for key in keys:
			self.CheckDoc(key)
	
	def CheckDoc(self, DocID):
		if L.Config('Loglevel') >= 3:
			Log('Running Lintadas on document ' + str(DocID))
		Doc = L.Docs[int(DocID)]
		assert not Doc == None
		Doc.Errors.Clear()

		# Test document files
		keys = Doc.Files.keys()
		for key in keys:

			File = Doc.Files[key]

			# Determine file format
			ext = File.Filename[-5:]
			ext = ext.upper()
			if ext == '.SGML':
				File.Format = "SGML"
				Doc.Format = 'SGML'
			elif ext[-4:] == '.XML':
				File.Format = "XML"
				Doc.Format = 'XML'
			elif ext[-3:] == '.WT':
				File.Format = 'WIKI'
				Doc.Format = 'WIKI'
			else:
				File.Format = ''
				Doc.Format = ''

			# Determine DTD for SGML and XML files
			if File.Format == 'XML' or File.Format == 'SGML':
				DTDVersion = ''
				try:
					command = 'grep -i DOCTYPE ' + cvs_root + File.Filename + ' | head -n 1'
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


			Doc.Save()
			File.Save()
		Log('Lintadas run on document ' + str(DocID) + ' complete')


# When run at the command line, check the document requested.
# If no document was specified, all checks are performed on all documents.
# 

Lintadas = Lintadas()

def main():
	import getopt
	import sys

	Docs = sys.argv[1:]
	if len(Docs) == 0:
		print "Running on all documents..."
		Lintadas.CheckAllDocs()
	else:
		for Doc in Docs:
			Lintadas.CheckDoc(Doc)

def usage():
	print "HTML.py version " + VERSION
	print
	print "This is part of the Lampadas System"
	print
	print "Pass doc ids to run Lintadas on specific docs,"
	print "or call with no parameters to run Lintadas on all docs."
	print


if __name__ == "__main__":
	main()
