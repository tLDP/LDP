from Globals import YES, NO
from base import DataManager

class Page(DataManager):

    def __init__(self):
        DataManager.__init__(self, 'page',
            {'page_code':           {'key_field': YES, 'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': '', 'attribute': 'code'},
             'section_code':        {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'section.section_code'},
             'sort_order':          {'key_field': NO,  'data_type': 'int',      'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'template_code':       {'key_field': NO,  'data_type': 'string',   'nullable': NO,  'i18n': NO,  'foreign_key': 'template.template_code'},
             'data':                {'key_field': NO,  'data_type': 'list',     'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'only_dynamic':        {'key_field': NO,  'data_type': 'bool',     'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'only_registered':     {'key_field': NO,  'data_type': 'bool',     'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'only_admin':          {'key_field': NO,  'data_type': 'bool',     'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'only_sysadmin':       {'key_field': NO,  'data_type': 'bool',     'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'created':             {'key_field': NO,  'data_type': 'created',  'nullable': NO,  'i18n': NO,  'foreign_key': ''},
             'updated':             {'key_field': NO,  'data_type': 'updated',  'nullable': NO,  'i18n': NO,  'foreign_key': ''}})

    def synch(self):
        last_synched = self.last_synched
        super(Page, self).synch()

        # Synchronize with i18n cache.
        self.dms.page_i18n.synch()
        i18ns = self.dms.page_i18n.get_by_keys([['updated', '>=', last_synched]])
        for key in i18ns.keys():
            i18n = i18ns[key]
            mine = self.get_by_id(i18n.code)
            if hasattr(mine, 'i18n'):
                delattr(mine, 'i18n')
