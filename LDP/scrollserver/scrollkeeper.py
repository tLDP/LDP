import sys, os, commands, string
from xml.dom.minidom import parse
import urllib

def FileContents(filename):
	f = open(filename, "r")
	text = f.read()
	f.close
	return text


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
					if child.nodeName == "docformat":
						for text in child.childNodes:
							self.Format = self.Format + text.nodeValue
					if child.nodeName == "toc":
						self.TOC.loadDOM(child)
		else:
			print "ERROR, not a document"


	def Prepare(self):
		if self.Format == "text/sgml":
			print "Processing " + self.SourceFile
			
			# only needed for remote documents, 
			# but harmless
			sgmlfile = urllib.urlretrieve(self.SourceFile)	

			sgmlfile = sgmlfile[0]
			xsl_stylesheet = "/usr/share/sgml/docbook/xsl-stylesheets-1.29/html/docbook.xsl"
                        xsl_stylesheet = "/home/david/scrollserver/stylesheets/docbook/docbook.xsl"

			cmd = "cd /var/cache/scrollserver; mkdir " + self.ID + "; cd " + self.ID + "; xsltproc --docbook --timing " + xsl_stylesheet + " " + sgmlfile + " > index.html"

			#print cmd
			os.system(cmd)

	def URL(self):
		if self.Format == "text/html":
			text = self.SourceFile
			if text[:5] == "http://" or text[:6] == "file://":
				pass
			else:
				text = "file://" + text
			#print text
			return text
		else:
			url = "docid?" + str(self.ID)
		return url

	def Link(self):
		html = "<a href=" + self.URL() + ">" + self.Title + "</a>"
		html += " (" + self.Format + ")"
		return html

	def HTML(self):
		if self.Format == "text/sgml":
			htmlfile = "/var/cache/scrollserver/" + self.ID + "/index.html"

			# Comment this, uncomment below to enable caching.
			self.Prepare()
			
#			if not os.path.isfile(htmlfile):
#				self.Prepare()
#			elif os.stat(htmlfile)[9] < os.stat(self.SourceFile)[9]:
#				self.Prepare()

			text = FileContents(htmlfile)
			
		else:
			text = "Sorry, I don't even know what (" + self.Format + ") is!"
		return text


class Section:

	Level = 0
	Title = ""
	Sections = []
	Documents = []

	hasHTML = 0
	html_loaded = 0
	html = ""

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

	def HTML(self):
		if self.html_loaded == 0:

			self.html = ""
			
			# See if any subsections generate HTML
			for sect in self.Sections:
				if sect.HTML() <> "":
					self.hasHTML = 1

			# See if any documents generate HTML
			for document in self.Documents:
				if self.html <> "":
					self.html = self.html + "<br>"
				self.html = self.html + document.Link()
				self.hasHTML = 1
		
			# If there is HTML, add title section and subsections
			if self.hasHTML > 0:
				self.html = "<h" + str(self.Level) + ">" + self.Title + "</h" + str(self.Level) + ">" + self.html

				for sect in self.Sections:
					self.html = self.html + sect.HTML()
			
			self.html_loaded = 1
		return self.html

	def DocumentByID(self, docid):
		for document in self.Documents:
			if document.ID == docid:
				return document.HTML()
		for sect in self.Sections:
			text = sect.DocumentByID(docid)
			if text <> "":
				return text
		return ""
	


class ContentList:

	Sections = []

	html = ""
	
	
	def __init__(self):
		self.load()

	def load(self):
		self.Sections = []
		self.html = ""
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

	def HTML(self):
		if self.html == "":
			self.html = ""
			for sect in self.Sections:
				self.html = self.html + sect.HTML()
		return self.html

	def DocumentByID(self, docid):
		for sect in self.Sections:
			text = sect.DocumentByID(docid)
			if text <> "":
				return text
		return ""


class ScrollKeeper:

	content_list = ContentList()

	def ContentList(self):
		return self.content_list

	def DocumentByID(self, docid):
		return self.content_list.DocumentByID(docid)
