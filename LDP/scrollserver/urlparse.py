#!/usr/bin/python2

import string

class URI:
	URI = ""
	Protocol = ""
	Server = ""
	Port = ""
	Path = ""
	Filename = ""
	Parameter = ""
	Anchor = ""

	def __init__(self, uri):

		self.URI = uri
		if not uri:
			return
		
		temp = uri
		temp = string.split(temp,"#")
		if len(temp) > 1:
			self.Anchor = temp[1]
		temp = temp[0]
		
		temp = string.split(temp,"?")
		if len(temp) > 1:
			self.Parameter = temp[1]
		temp = temp[0]
		
		temp = string.split(temp,"/")
		if len(temp) > 1:
			self.Filename = string.join(temp[len(temp)-1:])
		temp = string.join(temp[:len(temp)-1],"/")

		if temp[:7] == "http://":
			self.Protocol = "http://"
			temp = temp[7:]

		# If the first character is /, there is no server or port.
		if temp[:1] == "/":
			self.Path = temp[1:]
		else:
			temp = string.split(temp,":")
			if len(temp) > 1:
				self.Port = temp[1]
			self.Server = temp[0]

#	This is a tricky area, so leave this for testing when problems arise
#	due to strange URIs.
#		print "URI: " + self.URI
#		print "Protocol: " + self.Protocol
#		print "Server: " + self.Server
#		print "Port: " + self.Port
#		print "Path: " + self.Path
#		print "Filename: [" + self.Filename + "]"
#		print "Parameter: " + self.Parameter
