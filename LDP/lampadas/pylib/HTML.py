#!/usr/bin/python

"""
Lampadas HTML Primitives Module

This module generates HTML primitives and web pages for the WWW front-end
to the Lampadas system.
"""

# Modules ##################################################################

import DataLayer


# Constants


# Globals

L = DataLayer.Lampadas()


# ComboFactory

class ComboFactory:

	def ClassesCombo(self, value, lang):

		self.combo = "<select name='class'>\n"
		for classfoo in L.Classes:
			if classfoo == None: break
			self.combo = self.combo + "<option "
			if classfoo.ID == value:
				self.combo = self.combo + "selected "
			self.combo = self.combo + "value='" + str(classfoo.ID) + "'>"
			self.combo = self.combo + classfoo.I18n[lang].Name
			self.combo = self.combo + "</option>\n"
		self.combo = self.combo + "</select>"
		return self.combo

	def DocsCombo(self, value):
		self.combo = "<select name='doc'>\n"
		for doc in L.Docs:
			if doc == None: break
			self.combo = self.combo + "<option "
			if doc.ID == value:
				self.combo = self.combo + "selected "
			self.combo = self.combo + "value='" + str(doc.ID) + "'>"
			self.combo = self.combo + doc.Title
			self.combo = self.combo + "</option>\n"
		self.combo = self.combo + "</select>"
		return self.combo


Factory = ComboFactory()
output = Factory.ClassesCombo(2,'EN')
print output

#if __name__ == "__main__":
