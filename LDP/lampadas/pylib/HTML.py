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


# Constants


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
		page = L.Strings['tpl-default'].I18n[lang].Text
		page = page.replace('|header|', L.Strings['header'].I18n[lang].Text)
		page = page.replace('|footer|', L.Strings['footer'].I18n[lang].Text)
		
		
		if key[:4] == 'doc/':
			docid = int(key[4:])
			Doc = L.Docs[docid]
			assert not Doc == None
			if Doc.Format=='SGML' or Doc.Format == 'XML':
				Files = Doc.Files
				if Files.Count() == 0:
					return "No file to process"
				elif Files.Count() > 1:
					return "Only single files supported right now"
				keys = Files.keys()
				for key in keys:
					File = Files[key]
					page = C.ConvertSGMLFile(cvs_root + File.Filename, File.Format)
			else:
				return "FORMAT NOT YET SUPPORTED"

		else:
			page = page.replace('|body|', L.Strings[key].I18n[lang].Text)
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


Factory = HTMLFactory()

# Sample low-level ComboBox, Classes
#output = Factory.Combo.Classes(2,'EN')
#print output

# Sample i18n page, About Lampadas
#output = Factory.Page('pg-about', 'EN')
#print output

# Sample SGML processing, LDP Reviewer HOWTO
#output = Factory.Page('doc/419', 'EN')
#print output

# Sample XML processing, Finnish HOWTO
output = Factory.Page('doc/68', 'EN')
print output


#if __name__ == "__main__":
