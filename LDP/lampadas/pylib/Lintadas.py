#!/usr/bin/python

"""
Lampadas Error Checking Module

This module performs all kinds of automatic checks on data in the database
and the source files it points to. Errors are logged in the
document_error table.
"""

# Modules ##################################################################


# Constants


# Globals


# Lintadas

class Lintadas:

	import Config
	import DataLayer
	import os

	Config = Config.Config()
	L = DataLayer.Lampadas()

	def CheckAllDocs(self):
		keys = self.L.Docs.keys()
		for key in keys:
			self.CheckDoc(key)
	
	def CheckDoc(self, DocID):
		self.L.Log(3, 'Running Lintadas on document ' + str(DocID))
		Doc = self.L.Docs[int(DocID)]
		assert not Doc == None
		Doc.Errs.Clear()

		# Test document files
		keys = Doc.Files.keys()
		for key in keys:

			File = Doc.Files[key]

			if File.Local:
				self.L.Log.Write(3, 'Checking filename ' + key)
			else:
				self.L.Log.Write(3, 'Skipping remote file ' + key)
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

			formatkeys = self.L.Formats.keys()
			for formatkey in formatkeys:
				if self.L.Formats[formatkey].I18n['EN'].Name == FileFormat:
					File.FormatID = formatkey
				if self.L.Formats[formatkey].I18n['EN'].Name == DocFormat:
					Doc.FormatID = formatkey
			
			self.L.Log.Write(3, 'file format is ' + FileFormat)
			
			# Determine DTD for SGML and XML files
			if FileFormat == 'XML' or FileFormat == 'SGML':
				DTDVersion = ''
				try:
					command = 'grep -i DOCTYPE ' + self.Config.CVSRoot + File.Filename + ' | head -n 1'
					grep = self.os.popen(command, 'r')
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

			self.L.Log.Write(3, 'doc dtd is ' + Doc.DTD)

			Doc.Save()
			File.Save()
		self.L.Log(3, 'Lintadas run on document ' + str(DocID) + ' complete')


# When run at the command line, check the document requested.
# If no document was specified, all checks are performed on all documents.
# 

def main():
	import getopt
	import sys

	Lintadas = Lintadas()

	Docs = sys.argv[1:]
	if len(Docs) == 0:
		print "Running on all documents..."
		Lintadas.CheckAllDocs()
	else:
		for Doc in Docs:
			Lintadas.CheckDoc(Doc)

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
