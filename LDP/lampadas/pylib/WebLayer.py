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
import string


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
            page = Page()
            page.load_row(row)
            self.data[page.code] = page

    def add(self, page_code, sort_order, section_code, template_code, only_dynamic, only_registered, only_admin, only_sysadmin, data):
        sql = 'INSERT INTO page(page_code, sort_order, section_code, template_code, only_dynamic, only_registered, only_admin, only_sysadmin, data) '
        sql += 'VALUES (' + wsq(page_code) + ', ' + str(sort_order) + ', ' + wsq(section_code) + ', ' + wsq(template_code) + ', ' + wsq(bool2tf(only_dynamic)) + ', ' + wsq(bool2tf(only_registered)) + ', ' + wsq(bool2tf(only_admin)) + ', ' + wsq(bool2tf(only_sysadmin)) + ', ' + wsq(string.join(data)) + ')'
        db.runsql(sql)
        db.commit()
        page = Page(page_code)
        self.data[page.code] = page
        return page

    def adjust_sort_order(self, page_code, adjust_by):
        """
        Bump a page up or down an arbitrary number of positions in the sort order.
        If the sort_order reaches the top or bottom (0), it stops.
        """

        page = self[page_code]

        # You cannot adjust if the page is not in a section!
        if page.section_code=='':
            return

        # Determine whether to raise or lower sort_order
        if adjust_by > 0:
            adjust_tick = 1
        else:
            adjust_tick = -1
            
        adjustments = 0
        while adjustments <> adjust_by:

            # Find the document with which we will be switching.
            # Abort if there is no such creature.
            page_to_switch = self.find_by_sort_order(page.section_code, page.sort_order + adjust_tick)
            if page_to_switch==None:
                break

            # Put the other page in our place, and save it.
            page_to_switch.sort_order = page_to_switch.sort_order - adjust_tick
            page_to_switch.save()
            
            # Put ourselves in its place, and remember it.
            page.sort_order = page.sort_order + adjust_tick
            adjustments = adjustments + adjust_tick
            
            # Stop if we raach 0
            if page.sort_order==0:
                break

        # If we made any adjustments, save them.
        if adjustments <> 0:
            page.save()

    def find_by_sort_order(self, section_code, sort_order):
        for key in self.keys():
            page = self[key]
            if page.section_code==section_code and page.sort_order==sort_order:
                return page
        
        
class Page:

    def __init__(self, page_code='', sort_order=0, section_code='', template_code='', only_dynamic=0, only_registered=0, only_admin=0, only_sysadmin=0, data=[]):
        self.code            = page_code
        self.sort_order      = sort_order
        self.section_code    = section_code
        self.template_code   = template_code
        self.only_dynamic    = only_dynamic
        self.only_registered = only_registered
        self.only_admin      = only_admin
        self.only_sysadmin   = only_sysadmin
        self.data            = data
        self.title = LampadasCollection()
        self.menu_name = LampadasCollection()
        self.page = LampadasCollection()
        self.version = LampadasCollection()
        if page_code > '':
            self.load()

    def load(self):
        sql = 'SELECT page_code, section_code, sort_order, template_code, data, only_dynamic, only_registered, only_admin, only_sysadmin FROM page WHERE page_code=' + wsq(self.code)
        cursor = db.select(sql)
        row = cursor.fetchone()
        if row==None: return
        self.load_row(row)
        
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
        sql = "SELECT lang, title, menu_name, page, version FROM page_i18n WHERE page_code=" + wsq(self.code)
        cursor = db.select(sql)
        while (1):
            row = cursor.fetchone()
            if row==None: break
            lang            = row[0]
            self.title[lang] = trim(row[1])
            self.menu_name[lang] = trim(row[2])
            self.page[lang] = trim(row[3])
            self.version[lang] = trim(row[4])

            # if there's no menu_name, use the title by default
            if self.menu_name[lang]=='':
                self.menu_name[lang] = self.title[lang]

    def add_lang(self, lang, title, menu_name, page, version):
        sql = 'INSERT INTO page_i18n(page_code, lang, title, menu_name, page, version) VALUES (' + wsq(self.code) + ', ' + wsq(lang) + ', ' + wsq(title) + ', ' + wsq(menu_name) + ', ' + wsq(page) + ', ' + wsq(version) + ')'
        db.runsql(sql)
        db.commit()
        self.title[lang] = title
        self.menu_name[lang] = menu_name
        self.page[lang] = page
        self.version[lang] = version

    def save(self):
        sql = 'UPDATE page SET section_code=' + wsq(self.section_code) + ', sort_order=' + str(self.sort_order) + ', template_code=' + wsq(self.template_code) + ', data=' + wsq(string.join(self.data)) + ', only_dynamic=' + wsq(bool2tf(self.only_dynamic)) + ', only_registered=' + wsq(bool2tf(self.only_registered)) + ', only_admin=' + wsq(bool2tf(self.only_admin)) + ', only_sysadmin=' + wsq(bool2tf(self.only_sysadmin)) + ' WHERE page_code=' + wsq(self.code)
        db.runsql(sql)
        db.commit()
        for lang in self.title.keys():
            sql = 'UPDATE page_i18n SET title=' + wsq(self.title[lang]) + ', menu_name=' + wsq(self.menu_name[lang]) + ', page=' + wsq(self.page[lang]) + ', version=' + wsq(self.version[lang]) + ' WHERE page_code=' + wsq(self.code) + ' AND lang=' + wsq(lang)
            db.runsql(sql)
            db.commit()


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

    def add(self, pub_date=now_string()):
        news = NewsItem()
        news.id = db.next_id('news', 'news_id')
        news.pub_date = pub_date
        self[news.id] = news
        sql = 'INSERT INTO news(news_id, pub_date) VALUES (' + str(news.id) + ', ' + wsq(news.pub_date) + ')'
        db.runsql(sql)
        db.commit()
        return news
    
class NewsItem:

    def __init__(self, id=0, pub_date=None):
        self.id       = id
        if pub_date==None:
            self.pub_date = now_string()
        else:
            self.pub_date = pub_date
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

    def add_lang(self, lang, news):
        sql = 'INSERT INTO news_i18n(news_id, lang, news) VALUES (' + str(self.id) + ', ' + wsq(lang) + ', ' + wsq(news) + ')'
        db.runsql(sql)
        db.commit()
        self.news[lang] = news

    def save(self):
        sql = 'UPDATE news SET pub_date=' + wsq(self.pub_date) + ' WHERE news_id=' + str(self.id)
        db.runsql(sql)
        db.commit()
        for lang in self.news.keys():
            sql = 'UPDATE news_i18n SET news=' + wsq(self.news[lang]) + ' WHERE news_id=' + str(self.id) + ' AND lang=' + wsq(lang)
            db.runsql(sql)
            db.commit()
        

# FileReports

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

