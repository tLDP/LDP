#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class Page(Persistence):

    def __str__(self):
        return 'persistence.Page: %s' % (self.code)

    def __getattr__(self, attribute):
        if attribute=='untranslated_lang_keys':
            untranslated = []
            supported_langs = self.dms.language.get_by_keys([['supported', '=', 't']])
            for key in supported_langs.keys():
                if key not in self.title.keys():
                    untranslated.append(key)
            return untranslated
        elif attribute=='template':
            return self.dms.template.get_by_id(self.template_code)
        elif attribute=='section':  
            return self.dms.section.get_by_id(self.section_code)
        elif attribute=='i18n':
            self.i18n = self.dms.page_i18n.get_by_keys([['code', '=', self.code]])
            return self.i18n
        elif attribute=='title':
            title = LampadasCollection()
            for key in self.i18n.keys():
                i18n = self.i18n[key]
                title[i18n.lang] = i18n.title
            return title
        elif attribute=='menu_name':
            menu_name = LampadasCollection()
            for key in self.i18n.keys():
                i18n = self.i18n[key]
                if i18n.menu_name=='':
                    menu_name[i18n.lang] = i18n.title
                else:
                    menu_name[i18n.lang] = i18n.menu_name
            return menu_name
        elif attribute=='page':
            page = LampadasCollection()
            for key in self.i18n.keys():
                i18n = self.i18n[key]
                page[i18n.lang] = i18n.page
            return page
        elif attribute=='version':
            version = LampadasCollection()
            for key in self.i18n.keys():
                i18n = self.i18n[key]
                version[i18n.lang] = i18n.version
            return version
        else:
            raise AttributeError('No such attribute %s' % attribute)
