#!/usr/bin/python2.0

# Import required modules
#import sys
#import stat
#import string
#import commands
#import StringIO
#import locale
#import shutil
import os
from xml.dom.minidom import parse

					
class Address:
	"""
	Parse an <address> tag.
	"""
	
	Email = ""

	def loadDOM(self,dom):
		if dom.nodeType == 1 and dom.nodeName == "address":
			for child in dom.childNodes:
				if child.nodeType == 1 and child.nodeName == "email":
					self.Email = ""
					for text in child.childNodes:
						self.Email = self.Email + text.nodeValue
					
					
class Affiliation:
	"""
	Parse an <affiliation> tag.
	"""
	
	Address = Address()

	def loadDOM(self,dom):
		if dom.nodeType == 1 and dom.nodeName == "affiliation":
			for child in dom.childNodes:
				if child.nodeType == 1 and child.nodeName == "address":
					self.Address.loadDOM(child)

class OtherCredit:
	"""
	Parse an <othercredit> tag.
	"""
	
	Firstname = ""
	Surname = ""
	Contrib = ""

	def loadDOM(self,dom):
		if dom.nodeType == 1 and dom.nodeName == "othercredit":
			for child in dom.childNodes:
				if child.nodeType == 1 and child.nodeName == "firstname":
					for text in child.childNodes:
						self.Firstname = self.Firstname + text.nodeValue
				if child.nodeType == 1 and child.nodeName == "surname":
					for text in child.childNodes:
						self.Surname = self.Surname + text.nodeValue
				if child.nodeType == 1 and child.nodeName == "contrib":
					for text in child.childNodes:
						self.Contrib = self.Contrib + text.nodeValue


class Author:
	"""
	Parse an <author> tag.
	"""
	
	Firstname = ""
	Surname = ""
	Affiliation = Affiliation()

	def loadDOM(self,dom):
		if dom.nodeType == 1 and dom.nodeName == "author":
			for child in dom.childNodes:
				if child.nodeType == 1 and child.nodeName == "firstname":
					for text in child.childNodes:
						self.Firstname = self.Firstname + text.nodeValue
				if child.nodeType == 1 and child.nodeName == "surname":
					for text in child.childNodes:
						self.Surname = self.Surname + text.nodeValue
				if child.nodeType == 1 and child.nodeName == "affiliation":
					self.Affiliation.loadDOM(child)
					
					
class Revision:
	"""
	Parse a <revision> tag.
	"""

	Revnumber = ""
	Date = ""
	Revremark = ""

	def loadDOM(self,dom):
		if dom.nodeType == 1 and dom.nodeName == "revision":
			for child in dom.childNodes:
				if child.nodeType == 1 and child.nodeName == "revnumber":
					self.Revumber = ""
					for text in child.childNodes:
						self.Revnumber = self.Revnumber + text.nodeValue
				if child.nodeType == 1 and child.nodeName == "date":
					self.Date = ""
					for text in child.childNodes:
						self.Date = self.Date + text.nodeValue
				if child.nodeType == 1 and child.nodeName == "revremark":
					self.Revremark = ""
					for text in child.childNodes:
						self.Revremark = self.Revremark + text.nodeValue

class ArtHeader:
	"""
	Parse an <artheader> tag.
	"""
	
	Title = ""
	Authors = []
	OtherCredits = []
	Revisions = []
	Abstract = ""
	
	def loadDOM(self,dom):
		if dom.nodeType == 1 and dom.nodeName == "artheader":
			for child in dom.childNodes:
				if child.nodeType == 1 and child.nodeName == "title":
					self.Title = ""
					for text in child.childNodes:
						self.Title = self.Title + text.nodeValue
				if child.nodeType == 1 and child.nodeName == "author":
					newAuthor = Author()
					newAuthor.loadDOM(child)
					self.Authors = self.Authors + [newAuthor]
				if child.nodeType == 1 and child.nodeName == "othercredit":
					newOtherCredit = OtherCredit()
					newOtherCredit.loadDOM(child)
					self.OtherCredits = self.OtherCredits + [newOtherCredit]
				if child.nodeType == 1 and child.nodeName == "revhistory":
					for revision in child.childNodes:
						if revision.nodeType == 1 and revision.nodeName == "revision":
							newRevision = Revision()
							newRevision.loadDOM(revision)
							self.Revisions = self.Revisions + [newRevision]
				if child.nodeName == "abstract":
					for para in child.childNodes:
						if para.nodeType == 1 and para.nodeName == "para":
							for text in para.childNodes:
								self.Abstract = self.Abstract + text.nodeValue

class DocBook:
	"""
	Process a DocBook file into a DOM tree.
	"""
	
	Artheader = ArtHeader()
	Title = ""
	Authors = []
	Revisions = []
	OtherCredits = []

	def __init__(self,filename):
		self.load(filename)

	def load(self,filename):
		dom = parse(filename)
		self.loadDOM(dom.documentElement)

	def loadDOM(self,contents):
		for child in contents.childNodes:
			if child.nodeType == 1 and child.nodeName == "artheader":
				self.Artheader.loadDOM(child)
				self.Title = self.Artheader.Title
				self.Authors = self.Artheader.Authors
				self.OtherCredits = self.Artheader.OtherCredits
				self.Abstract = self.Artheader.Abstract
				self.Revisions = self.Artheader.Revisions

	
def db2db():
	"""
	Read the DocBook file and write out SQL statements.
	"""

	filename = "test.sgml"
	DB = DocBook(filename)

	# documents
	sql = ""
	sql = "UPDATE document SET "
	sql = sql + "title = '" + DB.Title + "' "
	sql = sql + "WHERE filename = '" + filename + "';"
	print sql
	#os.system("psql ldp -c " + sql)

#	for author in DB.Authors:
#		print "Author =",author.Affiliation.Address.Email, "(" + author.Firstname, author.Surname + ")"
#	for othercredit in DB.OtherCredits:
#		print "OtherCredit =",othercredit.Firstname, othercredit.Surname + ",", othercredit.Contrib
#	for revision in DB.Revisions:
#		print "Revision = ",revision.Revnumber, revision.Date, revision.Revremark
#	print "Abstract =", DB.Abstract

if __name__ == '__main__':
	db2db()
