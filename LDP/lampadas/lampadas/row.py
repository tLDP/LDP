#!/usr/bin/python

from twisted.enterprise import row
from types import *
from Globals import trim
from BaseClasses import LampadasCollection

def rowFactory(Klass, userData, kw):
    newObject = Klass()
    for key in kw.keys():
        value = kw[key]
        if type(value) is StringType:
            value = trim(value)
            kw[key] = value
    newObject.__dict__.update(kw)
    return newObject

class Block(row.RowObject):
    rowFactoryMethod = [rowFactory]
    rowTableName = 'block'
    rowKeyColumns = [('block_code', 'varchar')]
    rowColumns = [('block_code', 'varchar'),
                  ('block',      'varchar'),
                  ('created',    'timestamp'),
                  ('updated',    'timestamp')]

class Document(row.RowObject):
    rowFactoryMethod = [rowFactory]
    rowTableName = 'document'
    rowKeyColumns = [('doc_id', 'int')]
    rowColumns = [('doc_id',                    'int'),
                  ('lang',                      'varchar'),
                  ('title',                     'varchar'),
                  ('short_title',               'varchar'),
                  ('type_code',                 'varchar'),
                  ('format_code',               'varchar'),
                  ('dtd_code',                  'varchar'),
                  ('dtd_version',               'varchar'),
                  ('version',                   'varchar'),
                  ('last_update',               'timestamp'),
                  ('isbn',                      'varchar'),
                  ('pub_status_code',           'varchar'),
                  ('review_status_code',        'varchar'),
                  ('tickle_date',               'timestamp'),
                  ('pub_date',                  'timestamp'),
                  ('tech_review_status_code',   'varchar'),
                  ('maintained',                'bool'),
                  ('maintainer_wanted',         'bool'),
                  ('license_code',              'varchar'),
                  ('license_version',           'varchar'),
                  ('copyright_holder',          'varchar'),
                  ('abstract',                  'varchar'),
                  ('short_desc',                'varchar'),
                  ('rating',                    'int'),
                  ('sk_seriesid',               'int'),
                  ('replaced_by_id',            'int'),
                  ('lint_time',                 'timestamp'),
                  ('pub_time',                  'timestamp'),
                  ('mirror_time',               'timestamp'),
                  ('first_pub_date',            'timestamp'),
                  ('encoding',                  'varchar'),
                  ('created',                   'timestamp'),
                  ('updated',                   'timestamp')]

class Page(row.RowObject):
    rowFactoryMethod = [rowFactory]
    rowTableName = 'page'
    rowKeyColumns = [('page_code',    'varchar')]
    rowColumns = [('page_code',       'varchar'),
                  ('section_code',    'varchar'),
                  ('sort_order',      'int'),
                  ('template_code',   'varchar'),
                  ('data',            'varchar'),
                  ('only_dynamic',    'bool'),
                  ('only_registered', 'bool'),
                  ('only_admin',      'bool'),
                  ('only_sysadmin',   'bool')]

    def __init__(self):
        self.title = LampadasCollection()
        self.menu_name = LampadasCollection()
        self.page = LampadasCollection()
        self.version = LampadasCollection()
    
    def addI18n(self, i18n):
        lang = i18n.lang
        self.title[lang] = i18n.title
        self.menu_name[lang] = i18n.menu_name
        self.page[lang] = i18n.page
        self.version[lang] = i18n.version

class PageI18n(row.RowObject):
    rowFactoryMethod = [rowFactory]
    rowTableName = 'page_i18n'
    rowKeyColumns = [('page_code',  'varchar'),
                     ('lang',       'varchar')]
    rowColumns = [('page_code',     'varchar'),
                  ('lang',          'varchar'),
                  ('title',         'text'),
                  ('menu_name',     'text'),
                  ('page',          'text'),
                  ('version',       'varchar'),
                  ('created',       'timestamp'),
                  ('updated',       'timestamp')]
    rowForeignKeys = [('page', [('page_code', 'varchar')], [('page_code', 'varchar')], 'addI18n', 1)]

class Section(row.RowObject):
    rowFactoryMethod = [rowFactory]
    rowTableName = 'section'
    rowKeyColumns = [('section_code',   'varchar')]
    rowColumns = [('section_code',      'varchar'),
                  ('sort_order',        'int'),
                  ('only_dynamic',      'bool'),
                  ('created',           'timestamp'),
                  ('updated',           'timestamp')]

    def __init__(self):
        self.section_name = LampadasCollection()
    
    def addI18n(self, i18n):
        lang = i18n.lang
        self.section_name[lang] = i18n.section_name

class SectionI18n(row.RowObject):
    rowFactoryMethod = [rowFactory]
    rowTableName = 'section_i18n'
    rowKeyColumns = [('section_code',   'varchar'),
                     ('lang',           'varchar')]
    rowColumns = [('section_code',  'varchar'),
                  ('lang',          'varchar'),
                  ('section_name',  'varchar'),
                  ('created',       'timestamp'),
                  ('updated',       'timestamp')]
    rowForeignKeys = [('section', [('section_code', 'varchar')], [('section_code', 'varchar')], 'addI18n', 1)]

class String(row.RowObject):
    rowFactoryMethod = [rowFactory]
    rowTableName = 'string'
    rowKeyColumns = [('string_code', 'varchar')]
    rowColumns = [('string_code',   'varchar'),
                  ('created',       'timestamp'),
                  ('updated',       'timestamp')]
    
    def __init__(self):
        self.string = LampadasCollection()
        self.version = LampadasCollection()
    
    def addI18n(self, i18n):
        lang = i18n.lang
        self.string[lang] = i18n.string
        self.version[lang] = i18n.version

class StringI18n(row.RowObject):
    rowFactoryMethod = [rowFactory]
    rowTableName = 'string_i18n'
    rowKeyColumns = [('string_code', 'varchar'),
                     ('lang',        'varchar')]
    rowColumns = [('string_code',   'varchar'),
                  ('lang',          'varchar'),
                  ('string',        'varchar'),
                  ('version',       'varchar'),
                  ('created',       'timestamp'),
                  ('updated',       'timestamp')]
    rowForeignKeys = [('string', [('string_code', 'varchar')], [('string_code', 'varchar')], 'addI18n', 1)]


ROW_CLASSES = [Block, Document, Page, PageI18n, Section, SectionI18n, String, StringI18n]

