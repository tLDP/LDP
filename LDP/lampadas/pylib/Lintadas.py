#!/usr/bin/python

"""
Lampadas Error Checking Module

This module performs all kinds of automatic checks on data in the database
and the source files it points to. Errors are logged in the
document_error table.
"""

# Modules ##################################################################

import DataLayer


# Constants


# Globals

L = DataLayer.Lampadas()


# Lintadas

class Lintadas:

	def CheckAllDocs(self):
		keys = L.Docs.keys()
		for key in keys:
			self.CheckDocument(key)
	
	def CheckDocument(self, DocID):
		Doc = L.Docs[DocID]
		Doc.Errors.Clear()

		# Test document files
		keys = Doc.Files.keys()
		for key in keys:

			# Determine file format
			ext = Doc.Files[key].Filename[-5:]
			ext = ext.upper()
			if ext == '.SGML':
				Doc.Files[key].Format = "SGML"
			elif ext[-4:] == '.XML':
				Doc.Files[key].Format = "XML"
			elif ext[-3:] == '.WT':
				Doc.Files[key].Format = 'WIKI'
			else:
				Doc.Files[key].Format = ''
			Doc.Files[key].Save()


if __name__ == "__main__":
	Lintadas = Lintadas()
	Lintadas.CheckAllDocs()
