#!/usr/bin/python

"""
Lampadas HTML Primitives Module

This module generates HTML primitives and web pages for the WWW front-end
to the Lampadas system.
"""

# Modules ##################################################################

import DataLayer
import Converter
import commands
from types import *

# Constants

# These are string_id values for looking up strings in the string table
# 
PG_HEADER	= 2
PG_FOOTER	= 3

TPL_DEFAULT	= 1000
PG_ABOUT	= 2000


# Globals

L = DataLayer.Lampadas()
C = Converter.Converter()

cvs_root = L.Config('cvs_root')

# HTMLFactory

class HTMLFactory:

	def __init__(self):
		self.Page = PageFactory()
		self.Combo = ComboFactory()


# PageFactory

class PageFactory:

	def __call__(self, key, lang):
		if type(key) is IntType:
			return self.Page(key, lang)
		elif key[:4] == 'doc/':
			DocID = int(key[4:])
			return self.DocPage(DocID, lang)

	def Page(self, key, lang):
		page = L.Strings[TPL_DEFAULT].I18n[lang].Text
		page = page.replace('|header|', L.Strings[PG_HEADER].I18n[lang].Text)
		page = page.replace('|footer|', L.Strings[PG_FOOTER].I18n[lang].Text)
		page = page.replace('|body|', L.Strings[key].I18n[lang].Text)
		return page

	def DocPage(self, DocID, lang):
		Doc = L.Docs[DocID]
		assert not Doc == None
		docformat = L.Formats[Doc.FormatID].I18n['EN'].Name
		if docformat=='SGML' or docformat=='XML':
			Files = Doc.Files
			if Files.Count() == 0:
				page = 'No file to process'
			elif Files.Count() > 1:
				page = 'Only single files supported right now'
			else:
				keys = Files.keys()
				for key in keys:
					File = Files[key]
					page = C.ConvertSGMLFile(cvs_root + File.Filename, docformat)
		else:
			page =  'FORMAT ' + docformat  + ' NOT YET SUPPORTED'
		return page


# ComboFactory

class ComboFactory:

	def Classes(self, value, lang):

		self.combo = "<select name='class'>\n"
		keys = L.Classes.keys()
		for key in keys:
			classfoo = L.Classes[key]
			if classfoo == None: break
			self.combo = self.combo + "<option "
			if classfoo.ID == value:
				self.combo = self.combo + "selected "
			self.combo = self.combo + "value='" + str(classfoo.ID) + "'>"
			self.combo = self.combo + classfoo.I18n[lang].Name
			self.combo = self.combo + "</option>\n"
		self.combo = self.combo + "</select>"
		return self.combo

	def Docs(self, value, lang=None):
		self.combo = "<select name='doc'>\n"
		keys = L.Docs.keys()
		for key in keys:
			doc = L.Docs[key]
			if doc == None: break
			if doc.LanguageCode == lang or lang == None:
				self.combo = self.combo + "<option "
				if doc.ID == value:
					self.combo = self.combo + "selected "
				self.combo = self.combo + "value='" + str(doc.ID) + "'>"
				self.combo = self.combo + doc.Title
				self.combo = self.combo + "</option>\n"
		self.combo = self.combo + "</select>"
		return self.combo

	def DTDs(self, value, lang=None):
		self.combo = "<select name='dtd'>\n"
		keys = L.DTDs.keys()
		for key in keys:
			dtd = L.DTDs[key]
			if dtd == None: break
#			if dtd.LanguageCode == lang or lang == None:
			self.combo = self.combo + "<option "
			if dtd.DTD == value:
				self.combo = self.combo + "selected "
			self.combo = self.combo + "value='" + dtd.DTD + "'>"
			self.combo = self.combo + dtd.DTD
			self.combo = self.combo + "</option>\n"
		self.combo = self.combo + "</select>"
		return self.combo
	
	def Formats(self, value, lang=None):
		self.combo = "<select name='format'>\n"
		keys = L.Formats.keys()
		for key in keys:
			format = L.Formats[key]
			if format == None: break
			self.combo = self.combo + "<option "
			if format.ID == value:
				self.combo = self.combo + "selected "
			self.combo = self.combo + "value='" + str(format.ID) + "'>"
			self.combo = self.combo + format.I18n[lang].Name
			self.combo = self.combo + "</option>\n"
		self.combo = self.combo + "</select>"
		return self.combo


Factory = HTMLFactory()

# Sample low-level ComboBox, Classes
output = Factory.Combo.Classes(2, 'EN')
print output

# Sample low-level ComboBox, DTDs
output = Factory.Combo.DTDs(1, 'EN')
print output

# Sample low-level ComboBox, Formats
output = Factory.Combo.Formats(1, 'EN')
print output

# Sample i18n page, About Lampadas
output = Factory.Page(PG_ABOUT, 'EN')
print output

# Sample SGML processing, LDP Reviewer HOWTO
output = Factory.Page('doc/419', 'EN')
print output

# Sample XML processing, Finnish HOWTO
output = Factory.Page('doc/68', 'EN')
print output


#if __name__ == "__main__":
