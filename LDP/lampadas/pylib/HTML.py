#!/usr/bin/python

"""
Lampadas HTML Primitives Module

This module generates HTML primitives and web pages for the WWW front-end
to the Lampadas system.
"""

# Modules ##################################################################

from Globals import *
from Config import Config
import Database
from DataLayer import *
import WebLayer
from Converter import Converter
import commands
from string import split
import sys

# Globals

Config = Config()
L = Lampadas()
C = Converter()

cvs_root = L.Config('cvs_root')


# HTMLFactory

class HTMLFactory:

	def __init__(self):
		self.Reload()

	def Reload(self):
		self.Page = PageFactory()
		self.Combo = ComboFactory()


# BoxFactory

class BoxFactory:

	def MainMenu(self, lang):
		self.box = ''
		self.box = self.box + '<table><tr><th>|mmtitle|</th></tr>'
		self.box = self.box + '<tr><td>'
		self.box = self.box + '<a href="home">|home|</a>'
		self.box = self.box + '</td></tr>'
		self.box = self.box + '</table>'
		return self.box


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


# PageFactory

class PageFactory:

	Blocks		= WebLayer.Blocks()
	Pages		= WebLayer.Pages()
	Strings		= WebLayer.Strings()
	Templates	= WebLayer.Templates()
	Box		= BoxFactory()

	def __call__(self, key, lang):
		return self.Page(key, lang)

	def Page(self, key, lang):
		if key == '' or key == '/':
			key='home'
		if key[0] == '/':
			key = key[1:]
		Keys = split(key, '/')
		
		# Allow the language to be specified in the URL
		# 
		if Keys[0] in L.Languages.keys():
			if L.Languages[Keys[0]].Supported:
				lang = Keys[0]
			Keys = Keys[1:]
			
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
			page = page.replace('|title|', Page.I18n[lang].Title)
			page = page.replace('|body|', Page.I18n[lang].Page)

			page = page.replace('\|', 'DCM_PIPE')

			page = page.replace('|header|', self.Blocks['header'].I18n[lang].Block)
			page = page.replace('|footer|', self.Blocks['footer'].I18n[lang].Block)
			
			page = page.replace('\|', 'DCM_PIPE')
			
			pos = page.find('|')
			while pos <> -1 :
				pos2 = page.find('|', pos+1)
				if pos2 == -1:
					pos = -1
				else:
					oldstring = page[pos:pos2+1]
					token = page[pos+1:pos2]
					
					if token=='mainmenu':
						newstring = self.Box.MainMenu(lang)
					
					else:
						newstring = ''
						Block = self.Blocks[token]
						if Block == None:
							String = self.Strings[token]
							if String == None:
								newstring = 'ERROR'
								Log(1, 'Could not replace token ' + token)
							else:
								newstring = String.I18n[lang].String
						else:
							newstring = Block.I18n[lang].Block
					
					if newstring == '':
						Log(1, 'Could not replace token ' + token)
						
					page = page.replace(page[pos:pos2+1], newstring)
					
					page = page.replace('\|', 'DCM_PIPE')
					
					pos = page.find('|')
			
			page = page.replace('DCM_PIPE', '|')
			
		return page

	def DocPage(self, DocID, lang):
		Doc = L.Docs[DocID]
		if Doc == None:
			page = "Error, could not locate document " + str(DocID)
		else:
			docformat = L.Formats[Doc.FormatID].I18n[lang].Name
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


def main():
	F = PageFactory()
	for arg in sys.argv[1:]:
		print F.Page(arg, 'EN')

def usage():
	print "HTML.py version " + VERSION


if __name__ == "__main__":
	main()
