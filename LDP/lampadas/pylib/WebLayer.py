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
        sql = "SELECT block_code, block FROM block"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            newBlock = Block()
            newBlock.load_row(row)
            self.data[newBlock.code] = newBlock

class Block:

    def __init__(self):
        self.block = LampadasCollection()

    def load_row(self, row):
        self.code  = trim(row[0])
        self.block = trim(row[1])


# Sections

class Sections(LampadasCollection):

    def __init__(self):
        self.data = {}
        sql = "SELECT section_code, sort_order FROM section"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            newSection = Section()
            newSection.load_row(row)
            self.data[newSection.code] = newSection

class Section:

    def __init__(self):
        self.name = LampadasCollection()

    def load_row(self, row):
        self.code		      = trim(row[0])
        self.sort_order       = safeint(row[1])
        self.static_count    = int(db.read_value('SELECT COUNT(*) FROM page WHERE section_code=' + wsq(self.code) + ' AND only_dynamic=' + wsq('f') + ''))
        self.nonregistered_count = int(db.read_value('SELECT COUNT(*) FROM page WHERE section_code=' + wsq(self.code) + ' AND only_registered=' + wsq('f') + ' AND only_admin=' + wsq('f') + ' AND only_sysadmin=' + wsq('f') + ''))
        self.nonadmin_count      = int(db.read_value('SELECT COUNT(*) FROM page WHERE section_code=' + wsq(self.code) + ' AND only_admin=' + wsq('f') + ' AND only_sysadmin=' + wsq('f') + ''))
        self.nonsysadmin_count   = int(db.read_value('SELECT COUNT(*) FROM page WHERE section_code=' + wsq(self.code) + ' AND only_sysadmin=' + wsq('f') + ''))
        print self.code + ': ' + str(self.nonregistered_count) + ', ' + str(self.nonsysadmin_count) + ', ' + str(self.nonadmin_count)
        sql = "SELECT lang, section_name FROM section_i18n WHERE section_code=" + wsq(self.code)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            lang = row[0]
            self.name[lang] = trim(row[1])


# Pages

class Pages(LampadasCollection):

    def __init__(self):
        self.data = {}
        sql = "SELECT page_code, section_code, sort_order, template_code, data, only_dynamic, only_registered, only_admin, only_sysadmin FROM page"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            newPage = Page()
            newPage.load_row(row)
            self.data[newPage.code] = newPage

class Page:

    def __init__(self):
        self.title = LampadasCollection()
        self.menu_name = LampadasCollection()
        self.page = LampadasCollection()

    def load_row(self, row):
        self.code            = trim(row[0])
        self.section_code	 = trim(row[1])
        self.sort_order      = safeint(row[2])
        self.template_code	 = trim(row[3])
        self.data            = trim(row[4]).split()
        self.only_dynamic    = tf2bool(row[5])
        self.only_registered = tf2bool(row[6])
        self.only_admin      = tf2bool(row[7])
        self.only_sysadmin   = tf2bool(row[8])
        sql = "SELECT lang, title, menu_name, page FROM page_i18n WHERE page_code=" + wsq(self.code)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            lang            = row[0]
            self.title[lang] = trim(row[1])
            self.menu_name[lang] = trim(row[2])
            self.page[lang] = trim(row[3])
            if self.menu_name[lang]=='':
                self.menu_name[lang] = self.title[lang]


# Strings

class Strings(LampadasCollection):
    """
    A collection object of all localized strings.
    """
    
    def __init__(self):
        self.data = {}
        sql = "SELECT string_code FROM string"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            newString = String()
            newString.load_row(row)
            self.data[newString.code] = newString

class String:
    """
    Each string is Unicode text, that can be used in a web page.
    """

    def __init__(self, string_code=None):
        self.string = LampadasCollection()

    def load_row(self, row):
        self.code = trim(row[0])
        sql = "SELECT lang, string FROM string_i18n WHERE string_code=" + wsq(self.code)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            lang              = row[0]
            self.string[lang] = trim(row[1])


# Templates

class Templates(LampadasCollection):

    def __init__(self):
        self.data = {}
        sql = "SELECT template_code, template FROM template"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            newTemplate = Template()
            newTemplate.load_row(row)
            self.data[newTemplate.code] = newTemplate

class Template:

    def load_row(self, row):
        self.code       = trim(row[0])
        self.template   = trim(row[1])


# NewsItems

class NewsItems(LampadasCollection):

    def __init__(self):
        self.data = {}
        sql = "SELECT news_id, pub_date FROM news"
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            news = NewsItem()
            news.load_row(row)
            self.data[news.id] = news

class NewsItem:

    def __init__(self):
        self.news = LampadasCollection()

    def load_row(self, row):
        self.id       = row[0]
        self.pub_date = date2str(row[1])
        sql = "SELECT lang, news FROM news_i18n WHERE news_id=" + str(self.id)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            lang            = row[0]
            self.news[lang] = trim(row[1])


# NewsItems

class FileReports(LampadasCollection):

    def __init__(self):
        self.data = {}
        sql = 'SELECT report_code, only_cvs, command FROM file_report'
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            report = FileReport()
            report.load_row(row)
            self[report.code] = report
        sql = 'SELECT report_code, lang, report_name, report_desc FROM file_report_i18n'
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            report_code = trim(row[0])
            lang = trim(row[1])
            report = self[report_code]
            report.name[lang] = trim(row[2])
            report.description[lang] = trim(row[3])

class FileReport:

    def __init__(self):
        self.name = LampadasCollection()
        self.description = LampadasCollection()

    def load_row(self, row):
        self.code     = trim(row[0])
        self.only_cvs = tf2bool(row[1])
        self.command  = trim(row[2])


# WebLayer

class LampadasWeb:

    def __init__(self):
        self.blocks       = Blocks()
        self.sections     = Sections()
        self.pages        = Pages()
        self.strings      = Strings()
        self.templates    = Templates()
        self.news         = NewsItems()
        self.file_reports = FileReports()
        self.static       = 0


lampadasweb = LampadasWeb()

