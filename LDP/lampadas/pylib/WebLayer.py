#!/usr/bin/python

"""
Lampadas Web Objects Module

This module provides data objects (Templates, Pages, Blocks, and Strings) that
can be used to build the Lampadas website. All access to these objects
should come through this layer.
"""

# Modules ##################################################################

from Globals import *
from BaseClasses import *
import Config
import Database


# Globals

Config = Config.Config()
DB = Database.Database()
DB.Connect(Config.DBType, Config.DBName)


# Blocks

class Blocks(LampadasCollection):

	def __init__(self):
		self.data = {}
		self.sql = "SELECT block_code FROM block"
		self.cursor = DB.Select(self.sql)
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
		self.cursor = DB.Select(self.sql)
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


# Pages

class Pages(LampadasCollection):

	def __init__(self):
		self.data = {}
		self.sql = "SELECT page_code, template_code FROM page"
		self.cursor = DB.Select(self.sql)
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
		self.TemplateCode	= trim(row[1])
		self.sql = "SELECT lang, page FROM page_i18n WHERE page_code=" + wsq(self.Code)
		self.cursor = DB.Select(self.sql)
		while (1):
			self.row = self.cursor.fetchone()
			if self.row == None: break
			newPageI18n = PageI18n()
			newPageI18n.Load(self.row)
			self.I18n[newPageI18n.Lang] = newPageI18n

class PageI18n:

	def Load(self, row):
		self.Lang	= row[0]
		self.Page	= row[1]


# Strings

class Strings(LampadasCollection):
	"""
	A collection object of all localized strings.
	"""
	
	def __init__(self):
		self.data = {}
		self.sql = "SELECT string_code FROM string"
		self.cursor = DB.Select(self.sql)
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
		self.cursor = DB.Select(self.sql)
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
		self.cursor = DB.Select(self.sql)
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
