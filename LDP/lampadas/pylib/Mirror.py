#!/usr/bin/python

"""
Lampadas Mirroring Module

This module mirrors documents whose source files are located outside the
local Lampdas system.
"""

# Modules ##################################################################


# Constants


# Globals


class Mirror:

	from Config import Config
	from Lintadas import Lintadas
	import os.path
	import urllib
	import os

	C = Config()
	Lint = Lintadas()

	def mirror_all(self):
		dockeys = self.Lint.L.Docs.keys()
		for dockey in dockeys:
			self.mirror_doc(dockey)

	def mirror_doc(self, DocID):
		self.Doc = self.Lint.L.Docs[DocID]
		filekeys = self.Doc.Files.keys()
		for filekey in filekeys:
			self.File = self.Doc.Files[filekey]
			if not self.File.Local:
				self.filename = self.File.Filename
				self.Lint.L.Log(3, 'mirroring ' + self.filename)
				self.basename = self.os.path.basename(self.filename)
				self.localdir = self.C.cache_dir + str(self.Doc.ID) + '/'
				if not self.os.access(self.localdir, self.os.F_OK):
					self.os.mkdir(self.localdir)
				self.localname = self.localdir + self.basename
				self.urllib.urlretrieve(self.File.Filename, self.localname)
				command = 'cd ' + self.localdir + '; gunzip -f ' + self.basename
				self.os.system(command)
				filekeys = self.Doc.Files.keys()
				for filekey in filekeys:
					if self.Doc.Files[filekey].Local:
						self.Doc.Files[filekey].Del()
				for file in self.os.listdir(self.localdir):
					self.Doc.Files.Add(self.Doc.ID, file)
				self.Lint.CheckDoc(DocID)


if __name__ == "__main__":
	M = Mirror()
	M.mirror_all()

