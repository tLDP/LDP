#!/usr/bin/python

import os				# Import required modules
import sys
import stat
import string
import commands
import StringIO
import BaseHTTPServer
import shutil

from HTML import PageFactory
from Globals import VERSION

import StringIO

P = PageFactory()

BaseClass = BaseHTTPServer.BaseHTTPRequestHandler

class RequestHandler(BaseClass):
	"""
	Intercepts the HTTP requests and serves them.
	"""
	def do_GET(self):
		fd = self.send_head()
		if fd:
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			filesize = len(self.page)
			self.send_header('Content-length', filesize)
			self.end_headers()
			
			shutil.copyfileobj(fd, self.wfile)
			fd.close
	
	def do_HEAD(self):
		fd = self.send_head()
		fd.close()
	
	def send_head(self):
		"""
		Send the requested page.
		"""

		self.page = P.Page(self.path, 'EN')
		return StringIO.StringIO(self.page)


def WebServer():
	"""
	Initialize the server.
	"""
	interface = ''
	port = 8000

	print "Lampadas " + VERSION + " -- development version!"
	if interface != '':
		print '(Listening on interface %s, port %s)' % (interface, port)
	else:
		print '(Listening on all interfaces, port %s)' % port
	server = BaseHTTPServer.HTTPServer((interface, port), RequestHandler)
	server.serve_forever()

if __name__ == '__main__':
	WebServer()

