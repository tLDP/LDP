#!/usr/bin/python

from twisted.enterprise import row

class BlockRow(row.RowObject):
    rowColumns = [('block_code', 'varchar'),
                  ('block',      'varchar'),
                  ('created',    'timestamp'),
                  ('updated',    'timestamp')]
    rowKeyColumns = [('block_code', 'varchar')]
    rowTableName = 'block'

class PageRow(row.RowObject):
    rowColumns = [('page_code',       'varchar'),
                  ('section_code',    'varchar'),
                  ('sort_order',      'int'),
                  ('template_code',   'varchar'),
                  ('data',            'varchar'),
                  ('only_dynamic',    'bool'),
                  ('only_registered', 'bool'),
                  ('only_admin',      'bool'),
                  ('only_sysadmin',   'bool')]
    rowKeyColumns = [('page_code',    'varchar')]
    rowTableName = 'page'

class PageI18nRow(row.RowObject):
    rowColumns = [('page_code',     'varchar'),
                  ('lang',          'varchar'),
                  ('title',         'text'),
                  ('menu_name',     'text'),
                  ('page',          'text'),
                  ('version',       'varchar'),
                  ('created',       'timestamp'),
                  ('updated',       'timestamp')]
    rowKeyColumns = [('page_code',  'varchar'),
                     ('lang',       'varchar')]
    rowTableName = 'page_i18n'

