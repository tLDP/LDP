#!/usr/bin/python2


import os
import string
import commands
import StringIO
import locale
from urlparse import URI
import SimpleHTTPServer
import scrollkeeper


htmlbase  = "/var/cache/scrollserver/"	# This is the cache directory
caching   = 1 				# set to 1 to enable caching
xsltparam = "--timing"			# parameters to pass in all xsltproc calls
xsltparam = ""

lang = locale.setlocale(locale.LC_ALL)

BaseClass = SimpleHTTPServer.SimpleHTTPRequestHandler
ScrollKeeper = scrollkeeper.ScrollKeeper()

def FileContents(filename):
	f = open(filename, "r")
	text = f.read()
	f.close
	return text


def FileCache(sourcefile, htmlfile, cmd):
	if not os.path.exists(htmlfile) or caching == 0:
		os.system(cmd)


class RequestHandler(BaseClass):

	def do_GET(self):
		BaseClass.do_GET(self)

	def send_head(self):

		if self.path == "" or self.path == "/" or self.path == "/index.html":
			return self.send_Home()
		elif self.path == "/controls.html":
			return self.send_Controls()
		elif self.path == "/reset.html":
			return self.send_Reset()
		elif self.path == "/contents.html":
			return self.send_ContentsList()
		elif self.path =="/documents.html":
			return self.send_DocList()
		elif self.path == "/help.html":
			return self.send_Help()
		else:
			uri = URI(self.path)
		
			if uri.Filename == "docid":
				return self.send_DocumentByID(uri.Parameter)
			else:
				return self.send_URI(uri)

	def send_Home(self):
		FileCache ("", htmlbase+ "index.html", "xsltproc " + xsltparam + " stylesheets/index.xsl stylesheets/index.xsl > " + htmlbase + "index.html")
		return self.send_File(htmlbase + "index.html")
			
	def send_Help(self):
		FileCache ("", htmlbase+ "help.html", "xsltproc " + xsltparam + " stylesheets/help.xsl stylesheets/help.xsl > " + htmlbase + "help.html")
		return self.send_File(htmlbase + "help.html")
			
	def send_Controls(self):
		FileCache ("", htmlbase + "controls.html", "xsltproc " + xsltparam + " stylesheets/controls.xsl stylesheets/controls.xsl > " + htmlbase + "controls.html")
		return self.send_File(htmlbase + "controls.html")

	def send_Reset(self):
		os.system("rm -rf " + htmlbase + "*")
		FileCache ("", htmlbase + "reset.html", "xsltproc " + xsltparam + " stylesheets/reset.xsl stylesheets/reset.xsl > " + htmlbase + "reset.html")
		return self.send_File(htmlbase + "reset.html")

	def send_ContentsList(self):
		contents_list = commands.getoutput("scrollkeeper-get-content-list " + lang)
		FileCache (contents_list, htmlbase + "contents.html", "xsltproc " + xsltparam + " stylesheets/contents.xsl " + contents_list + " > " + htmlbase + "contents.html")
		return self.send_File(htmlbase + "contents.html")

	def send_DocList(self):
		contents_list = commands.getoutput("scrollkeeper-get-content-list " + lang)
		FileCache (contents_list, htmlbase + "documents.html", "xsltproc " + xsltparam + " stylesheets/documents.xsl " + contents_list + " > " + htmlbase + "documents.html")
		return self.send_File(htmlbase + "documents.html")

	def send_DocumentByID(self, docid):
		document = ScrollKeeper.DocumentByID(docid)
#		if not document:
#			text = "Error: ScrollServer couldn't find document number " + docid
#			return self.send_Text(text)
		
		xmlfile = document.SourceFile
		xmlpath =  os.path.dirname(xmlfile)
		htmlpath = htmlbase + docid
		htmlfile = htmlpath + "/index.html"

#		Uncomment to debug file and path problems
#		print "xmlpath:" + xmlpath
#		print "htmlpath:" + htmlpath
#		print "htmlfile:" + htmlfile
#		print "xmlfile:" + xmlfile
#		print "format:" + document.Format

		FileCache ("", htmlpath, "mkdir " + htmlpath)
		
		if document.Format == "text/sgml":
			FileCache (xmlfile, htmlfile, "xsltproc --docbook " + xsltparam + " stylesheets/docbook/docbook.xsl " + xmlfile + " > " + htmlfile)
			
		os.system("ln -s --target-directory=" + htmlpath + " " + xmlpath + "/*")
		return self.send_File(htmlfile)

	def send_URI(self, uri):

		filename = uri.Path + "/" + uri.Filename
		if os.path.isfile(filename):
			return self.send_File(filename)
			
		referer = self.headers.getheader("Referer")
		refuri = URI(referer)

		if refuri.Filename == "docid":
			document = ScrollKeeper.DocumentByID(refuri.Parameter)
			filename = htmlbase + document.ID + "/" + uri.Path + "/" + uri.Filename
			return self.send_File(filename)
		else:
			text = "Unrecognized request: " + uri.Filename
			return self.send_Text(text)

	def send_File(self, filename):
		temp = string.split(filename, ".")
		if len(temp) > 1:
			fileext = temp[1]
		else:
			fileext = ""
			if os.path.isfile(filename + ".png"):
				fileext = "png"
			elif os.path.isfile(filename + ".jpeg"):
				fileext = "jpeg"
			if os.path.isfile(filename + ".jpg"):
				fileext = "jpg"
			if os.path.isfile(filename + ".gif"):
				fileext = "gif"
			filename += "." + fileext
			
		if fileext == "html" or fileext == "htm":
			mimetype = "text/html"
		elif fileext == "png":
			mimetype = "image/png"
		elif fileext == "gif":
			mimetype = "image/gif"
		elif fileext == "jpg" or fileext == "jpeg":
			mimetype = "image/jpeg"
		elif fileext == "css":
			mimetype = "text/css"
		else:
			mimetype = "text/plain"

		if os.path.isfile(filename):
			self.send_response(200)
			self.send_header("Content-type", mimetype)
			self.end_headers()
			text = FileContents(filename)
		else:
			text = "Unrecognized file: " + filename			

		return StringIO.StringIO(text)

	def send_Text(self, text):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		return StringIO.StringIO(text)


def ScrollServer():
	os.system("rm -rf " + htmlbase + "*")
	print "ScrollServer v0.5 -- development version!"
	SimpleHTTPServer.test(RequestHandler)

ScrollServer()

