#import sys
#import os
import commands
#import string
#import urllib

from xml.dom.minidom import parse

class TOCSection:

	ID = ""
	Sections = []

	def loadDOM(self,dom):
		if dom.nodeType == 1 and dom.nodeName[0:7] == "tocsect":
			if dom.hasAttributes:
				for i in range(dom.attributes.length):
					attribute = dom.attributes.item(i)
					if attribute.name == "linkid":
						self.ID = attribute.value
			for child in dom.childNodes:
				if child.nodeType == 1 and child.nodeName[0:7] == "tocsect":
					newSection = TOCSection()
					newSection.loadDOM(child)
					self.Sections = self.Sections + [newSection]
		else:
			print "ERROR, not a TOC section"
		

class TOC:

	Sections = []
	
	def loadDOM(self,dom):
		if dom.nodeType == 1 and dom.nodeName == "toc":
			for child in dom.childNodes:
				if child.nodeType == 1 and child.nodeName[0:7] == "tocsect":
					newSection = TOCSection()
					newSection.loadDOM(child)
					self.Sections = self.Sections + [newSection]
		else:
			print "ERROR, not a TOC"


class Document:

	ID = 0
	Title = ""
	OMF = ""
	SourceFile = ""
	Format = ""
	URL = ""
	TOC = TOC()

	def loadDOM(self,dom):
		if dom.nodeType == 1 and dom.nodeName == "doc":
			if dom.hasAttributes:
				for i in range(dom.attributes.length):
					attribute = dom.attributes.item(i)
					if attribute.name == "docid":
						self.ID = attribute.value
			for child in dom.childNodes:
				if child.nodeType == 1:
					if child.nodeName == "doctitle":
						for text in child.childNodes:
							self.Title = self.Title + text.nodeValue
					if child.nodeName == "docomf":
						for text in child.childNodes:
							self.OMF = self.OMF + text.nodeValue
					if child.nodeName == "docsource":
						for text in child.childNodes:
							self.SourceFile = self.SourceFile + text.nodeValue
						self.URL = self.SourceFile
						if self.URL[:5] == "http://" or self.URL[:6] == "file://":
							pass
						else:
							self.URL = "file://" + self.URL
					if child.nodeName == "docformat":
						for text in child.childNodes:
							self.Format = self.Format + text.nodeValue
					if child.nodeName == "toc":
						self.TOC.loadDOM(child)
		else:
			print "ERROR, not a document"




class Section:

	Level = 0
	Title = ""
	Sections = []
	Documents = []

	def loadDOM(self,dom):
		if dom.nodeType == 1 and dom.nodeName == "sect":
			for child in dom.childNodes:
				if child.nodeType == 1:
					if child.nodeName == "title":
						self.Title = ""
						for text in child.childNodes:
							self.Title = self.Title + text.nodeValue
					elif child.nodeName == "sect":
						newSection = Section()
						newSection.Level = self.Level + 1
						newSection.loadDOM(child)
						self.Sections = self.Sections + [newSection]
					elif child.nodeName == "doc":
						newDocument = Document()
						newDocument.loadDOM(child)
						self.Documents = self.Documents + [newDocument]


	def DocumentByID(self, docid):
		for document in self.Documents:
			if document.ID == docid:
				return document
		for sect in self.Sections:
			document = sect.DocumentByID(docid)
			if not document == None:
				return document
		return None
	


class ContentList:

	Sections = []

	def __init__(self):
		self.load()

	def load(self):
		self.Sections = []
		cmd = "scrollkeeper-get-extended-content-list C"
		filename = commands.getoutput(cmd)
		dom = parse(filename)
		self.loadDOM(dom.documentElement)

	def loadDOM(self,contents):
		for sect in contents.childNodes:
			if sect.nodeType == 1 and sect.nodeName == "sect":
				newSection = Section()
				newSection.Level = 1
				newSection.loadDOM(sect)
				self.Sections = self.Sections + [newSection]

	def DocumentByID(self, docid):
		for sect in self.Sections:
			document = sect.DocumentByID(docid)
			if not document == None:
				return document
		return None


class ScrollKeeper:

	content_list = ContentList()

	def ContentList(self):
		return self.content_list

	def DocumentByID(self, docid):
		return self.content_list.DocumentByID(docid)
