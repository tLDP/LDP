#!/usr/bin/python

import string

class URI:
	URI = ""
	Protocol = ""
	Server = ""
	Port = ""
	Language = ""
	Path = ""
	Filename = ""
	Parameter = ""
	Anchor = ""

	def __init__(self, uri):

		self.URI = uri
		if not uri:
			return
		
		temp = uri
		
		if temp[:7] == "http://":
			self.Protocol = "http://"
			temp = temp[7:]

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
			self.Filename = temp[-1]
		temp = string.join(temp[:len(temp)-1],"/")

		temp = string.split(temp,"/")
		if len(temp) > 1:
			self.Path = string.join(temp[1:],'/') + '/'
		temp = temp[0]

		temp = string.split(temp,":")
		if len(temp) > 1:
			self.Port = temp[1]
			self.Server = temp[0]
		
		if len(self.Path) > 1:
			if len(self.Path) == 2:
				self.Language = self.Path
				self.Path = ''
			elif self.Path[2] == '/':
				self.Language = self.Path[:2]
				self.Path = self.Path[2:]


#	This is a tricky area, so leave this for testing when problems arise
#	due to strange URIs.
#		print "URI: [" + self.URI + "]"
#		print "Language: [" + self.Language + "]"
#		print "Protocol: [" + self.Protocol + "]"
#		print "Server: [" + self.Server + "]"
#		print "Port: [" + self.Port + "]"
#		print "Path: [" + self.Path + "]"
#		print "Filename: [" + self.Filename + "]"
#		print "Parameter: [" + self.Parameter + "]"
#		print "Anchor: [" + self.Anchor + "]"


if __name__ == '__main__':
	foo = URI('http://localhost:8000/EN/editdoc/1/home#foo')
