#!/usr/bin/python2

import os
import string
import commands
import StringIO
import SimpleHTTPServer
import scrollkeeper

BaseClass = SimpleHTTPServer.SimpleHTTPRequestHandler
ScrollKeeper = scrollkeeper.ScrollKeeper()

htmlbase = "/var/cache/scrollserver/"

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
			return self.send_ContentsList()
        	elif filename == "docid":
			return self.send_DocumentByID(parameter)
		else:
			print "Unrecognized request: " + self.path + " (" + filename + "," + parameter + ")"
			document = ScrollKeeper.ContentList()
			return BaseClass.send_head(self)
									        
	def send_ContentsList(self):
		if not os.path.isfile("contents-list.html"):
			cmd = "scrollkeeper-get-content-list C"
			contents_list = commands.getoutput(cmd)
			cmd = "xsltproc stylesheets/contents-list/contents-list.xsl " + contents_list + " > contents-list.html"
			os.system(cmd)
		return self.send_File("contents-list.html")

	def send_DocumentByID(self, docid):
		document = ScrollKeeper.DocumentByID(docid)

		if document.Format == "text/html":
			text = '<html><head><meta http-equiv="refresh" content="0; url=' + document.URL + '"></head></html>'
			print text
			return self.send_Text(text)
			
		
		xmlfile = document.SourceFile
		htmlpath = htmlbase + docid
		htmlfile = htmlpath + "/index.html"
		if not os.path.isfile(htmlfile):
			cmd = "mkdir " + htmlpath
			os.system(cmd)
			cmd = "xsltproc --docbook --timing stylesheets/docbook/docbook.xsl " + xmlfile + " > " + htmlfile
			os.system(cmd)
		return self.send_File(htmlfile)

	def send_File(self, filename):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
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

