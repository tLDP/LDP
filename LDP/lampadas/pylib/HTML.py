#!/usr/bin/python

"""
Lampadas HTML Primitives Module

This module generates HTML primitives and web pages for the WWW front-end
to the Lampadas system.
"""

# Modules ##################################################################

from Globals import *
import Config
import Database
import DataLayer
import WebLayer
import Converter
import commands
from string import split


# Globals

Config = Config.Config()
L = DataLayer.Lampadas()
C = Converter.Converter()
DB = Database.Database()
DB.Connect(Config.DBType, Config.DBName)

cvs_root = L.Config('cvs_root')


# HTMLFactory

class HTMLFactory:

	def __init__(self):
		self.Page = PageFactory()
		self.Combo = ComboFactory()


# PageFactory

class PageFactory:

	Blocks		= WebLayer.Blocks()
	Pages		= WebLayer.Pages()
	Strings		= WebLayer.Strings()
	Templates	= WebLayer.Templates()

	def __call__(self, key, lang):
		return self.Page(key, lang)

	def Page(self, key, lang):
		Keys = split(key, '/')
		pagecode = Keys[0]
		if pagecode == 'doc':
			DocID = int(Keys[1])
			page = self.DocPage(DocID, lang)
		else:
			Page = self.Pages[pagecode] 
			assert not Page == None
			Template = self.Templates[Page.TemplateCode]
			assert not Template == None
			page = Template.Template
			page = page.replace('|header|', self.Blocks['header'].I18n[lang].Block)
			page = page.replace('|body|', Page.I18n[lang].Page)
			page = page.replace('|footer|', self.Blocks['footer'].I18n[lang].Block)
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


#Factory = HTMLFactory()

# Sample low-level ComboBox, Classes
#output = Factory.Combo.Classes(2, 'EN')
#print output

# Sample low-level ComboBox, DTDs
#output = Factory.Combo.DTDs(1, 'EN')
#print output

# Sample low-level ComboBox, Formats
#output = Factory.Combo.Formats(1, 'EN')
#print output

# Sample i18n page, About Lampadas
#output = Factory.Page(PG_ABOUT, 'EN')
#print output

# Sample SGML processing, LDP Reviewer HOWTO
#output = Factory.Page('doc/419', 'EN')
#print output

# Sample XML processing, Finnish HOWTO
#output = Factory.Page('doc/68', 'EN')
#print output


#if __name__ == "__main__":
