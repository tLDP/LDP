#!/usr/bin/python
# 
# This file is part of the Lampadas Documentation System.
# 
# Copyright (c) 2000, 2001, 2002 David Merrill <david@lupercalia.net>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 
"""
Lampadas Web Objects Module

This module provides data objects (Templates, Pages, Blocks, and Strings) that
can be used to build the Lampadas website. All access to these objects
should come through this layer.
"""

# Modules ##################################################################

from Globals import *
from BaseClasses import *
from Config import config
from Database import db


# Globals



# Blocks

class Blocks(LampadasCollection):

	def __init__(self):
		self.data = {}
		self.sql = "SELECT block_code FROM block"
		self.cursor = db.select(self.sql)
		while (1):
			self.row = self.cursor.fetchone()
			if self.row == None: break
			newBlock = Block()
			newBlock.Load(self.row)
			self.data[newBlock.Code] = newBlock

class Block:

	def __init__(self):
		self.I18n = {}

	def Load(self, row):
		self.Code		= trim(row[0])
		self.sql = "SELECT lang, block FROM block_i18n WHERE block_code=" + wsq(self.Code)
		self.cursor = db.select(self.sql)
		while (1):
			self.row = self.cursor.fetchone()
			if self.row == None: break
			newBlockI18n = BlockI18n()
			newBlockI18n.Load(self.row)
			self.I18n[newBlockI18n.Lang] = newBlockI18n

class BlockI18n:

	def Load(self, row):
		self.Lang	= row[0]
		self.Block	= row[1]


# Sections

class Sections(LampadasCollection):

	def __init__(self):
		self.data = {}
		self.sql = "SELECT section_code FROM section"
		self.cursor = db.select(self.sql)
		while (1):
			self.row = self.cursor.fetchone()
			if self.row == None: break
			newSection = Section()
			newSection.Load(self.row)
			self.data[newSection.Code] = newSection

class Section:

	def __init__(self):
		self.I18n = {}

	def Load(self, row):
		self.Code		= trim(row[0])
		self.sql = "SELECT lang, section_name FROM section_i18n WHERE section_code=" + wsq(self.Code)
		self.cursor = db.select(self.sql)
		while (1):
			self.row = self.cursor.fetchone()
			if self.row == None: break
			newSectionI18n = SectionI18n()
			newSectionI18n.Load(self.row)
			self.I18n[newSectionI18n.Lang] = newSectionI18n

class SectionI18n:

	def Load(self, row):
		self.Lang	= row[0]
		self.Name	= trim(row[1])


# Pages

class Pages(LampadasCollection):

	def __init__(self):
		self.data = {}
		self.sql = "SELECT page_code, section_code, template_code FROM page"
		self.cursor = db.select(self.sql)
		while (1):
			self.row = self.cursor.fetchone()
			if self.row == None: break
			newPage = Page()
			newPage.Load(self.row)
			self.data[newPage.Code] = newPage

class Page:

	def __init__(self):
		self.I18n = {}

	def Load(self, row):
		self.Code		= trim(row[0])
		self.SectionCode	= trim(row[1])
		self.TemplateCode	= trim(row[2])
		self.sql = "SELECT lang, title, page FROM page_i18n WHERE page_code=" + wsq(self.Code)
		self.cursor = db.select(self.sql)
		while (1):
			self.row = self.cursor.fetchone()
			if self.row == None: break
			newPageI18n = PageI18n()
			newPageI18n.Load(self.row)
			self.I18n[newPageI18n.Lang] = newPageI18n

class PageI18n:

	def Load(self, row):
		self.Lang	= row[0]
		self.Title	= row[1]
		self.Page	= row[2]


# Strings

class Strings(LampadasCollection):
	"""
	A collection object of all localized strings.
	"""
	
	def __init__(self):
		self.data = {}
		self.sql = "SELECT string_code FROM string"
		self.cursor = db.select(self.sql)
		while (1):
			row = self.cursor.fetchone()
			if row == None: break
			newString = String()
			newString.Load(row)
			self.data[newString.Code] = newString

class String:
	"""
	Each string is Unicode text, that can be used in a web page.
	"""

	def __init__(self, StringCode=None):
		self.I18n = {}

	def Load(self, row):
		self.Code = trim(row[0])
		self.sql = "SELECT lang, string FROM string_i18n WHERE string_code=" + wsq(self.Code)
		self.cursor = db.select(self.sql)
		while (1):
			self.row = self.cursor.fetchone()
			if self.row == None: break
			newStringI18n = StringI18n()
			newStringI18n.Load(self.row)
			self.I18n[newStringI18n.Lang] = newStringI18n

# StringI18n

class StringI18n:

	def Load(self, row):
		self.Lang		= row[0]
		self.String		= trim(row[1])


# Templates

class Templates(LampadasCollection):

	def __init__(self):
		self.data = {}
		self.sql = "SELECT template_code, template FROM template"
		self.cursor = db.select(self.sql)
		while (1):
			self.row = self.cursor.fetchone()
			if self.row == None: break
			newTemplate = Template()
			newTemplate.Load(self.row)
			self.data[newTemplate.Code] = newTemplate

class Template:

	def Load(self, row):
		self.Code	= trim(row[0])
		self.Template	= trim(row[1])
