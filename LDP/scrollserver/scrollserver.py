#!/usr/bin/python2

import os
import string
import commands
import StringIO
import SimpleHTTPServer
import scrollkeeper

BaseClass = SimpleHTTPServer.SimpleHTTPRequestHandler
ScrollKeeper = scrollkeeper.ScrollKeeper()

htmlbase = "/var/cache/scrollserver/"	# This is the cache directory
caching = 1 				# set to 1 to enable caching
xsltparam = "--timing"			# parameters to pass in all xsltproc calls

def FileContents(filename):
	f = open(filename, "r")
	text = f.read()
	f.close
	return text

class MyRequestHandler(BaseClass):

	def do_GET(self):
		BaseClass.do_GET(self)

	def send_head(self):

		# extract parameter
		uri = string.split(self.path,"?")
		if len(uri) > 1:
			parameter = uri[1]
		else:
			parameter = ""

		# extract filename
		uri = string.split(uri[0],"/")
		if len(uri) > 1:
			directory = uri[0]
			filename = uri[1]
		else:
			directory = ""
			filename = uri[0]
		
		if self.path == "" or self.path == "/" or self.path == "/index.html":
			return self.send_Home()
		elif self.path == "/contents.html":
			return self.send_ContentsList()
		elif self.path =="/documents.html":
			return self.send_DocList()
        	elif filename == "docid":
			return self.send_DocumentByID(parameter)
		else:
			filename = string.split(self.path, "/")
			while len(filename) > 1:
				filename = filename[1:]
			filename = filename[0]
			if not os.path.isfile(filename):
				text = "Unrecognized request: " + filename
				print text
				return self.send_Text(text)
			return self.send_File(filename)

	def send_Home(self):
		if not os.path.isfile("index.html") or caching == 0:
			cmd = "xsltproc " + xsltparam + " stylesheets/index.xsl stylesheets/documents.xsl > index.html"
			os.system(cmd)
		return self.send_File("index.html")
			
	def send_ContentsList(self):
		if not os.path.isfile("contents.html") or caching == 0:
			cmd = "scrollkeeper-get-content-list C"
			contents_list = commands.getoutput(cmd)
			cmd = "xsltproc " + xsltparam + " stylesheets/contents.xsl " + contents_list + " > contents.html"
			os.system(cmd)
		return self.send_File("contents.html")

	def send_DocList(self):
		if not os.path.isfile("documents.html") or caching == 0:
			cmd = "scrollkeeper-get-content-list C"
			contents_list = commands.getoutput(cmd)
			cmd = "xsltproc " + xsltparam + " stylesheets/documents.xsl " + contents_list + " > documents.html"
			os.system(cmd)
		return self.send_File("documents.html")

	def send_DocumentByID(self, docid):
		document = ScrollKeeper.DocumentByID(docid)
		
		xmlfile = document.SourceFile
		xmlpath =  os.path.dirname(xmlfile)
		htmlpath = htmlbase + docid
		htmlfile = htmlpath + "/index.html"

		if document.Format == "text/html":
			text = '<html><head><meta http-equiv="refresh" content="0; url=' + document.URL + '"></head></html>'
			return self.send_Text(text)
		
		if not os.path.isfile(htmlfile) or caching == 0:
			cmd = "mkdir " + htmlpath
			os.system(cmd)
			cmd = "xsltproc --docbook " + xsltparam + " stylesheets/docbook/docbook.xsl " + xmlfile + " > " + htmlfile
			os.system(cmd)
		return self.send_File(htmlfile)

	def send_File(self, filename):
		fileext = string.split(filename, ".")[1]
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
		self.send_response(200)
		self.send_header("Content-type", mimetype)
		self.end_headers()
		text = FileContents(filename)
		return StringIO.StringIO(text)

	def send_Text(self, text):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		return StringIO.StringIO(text)
		

def ScrollServer():
	os.system("rm -rf /var/cache/scrollserver/*")
	os.system("rm *.html")
	SimpleHTTPServer.test(MyRequestHandler)

ScrollServer()

