#!/usr/bin/python2

import string
import StringIO
import SimpleHTTPServer
import scrollkeeper
 
BaseClass = SimpleHTTPServer.SimpleHTTPRequestHandler
ScrollKeeper = scrollkeeper.ScrollKeeper()
  
CounterTemplate = """ <H1>Server
Statistics</H1>
   
This <A HREF=./>server</A> has been accessed
<b>%d</b> times.  """
    
count = 0
     
class MyRequestHandler(BaseClass):

	def do_GET(self):
		global count
		count = count + 1
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
			return self.send_TOC()
		elif self.path == "/counter.html":
			return self.send_counter()
		elif self.path == "/reload":
			print "Reloading..."
			ScrollKeeper.ContentList().load()
			return self.send_TOC()
        	elif filename == "docid":
			return self.send_DocumentByID(parameter)
		else:
			print "Unrecognized request: " + self.path + " (" + filename + "," + parameter + ")"
			document = ScrollKeeper.ContentList()
			return BaseClass.send_head(self)
									        
	def send_TOC(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		text = ScrollKeeper.ContentList().HTML()
		return StringIO.StringIO(text)
															     
	def send_DocumentByID(self, docid):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		text = ScrollKeeper.DocumentByID(docid)
		return StringIO.StringIO(text)

	def send_counter(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		text = CounterTemplate % count
		return StringIO.StringIO(text)

def ScrollServer():
	SimpleHTTPServer.test(MyRequestHandler)

ScrollServer()  
 
