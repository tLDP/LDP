#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class Page(Persistence):

    def __getattr__(self, attribute):
        if attribute=='template':
            self.template = self.dms.template.get_by_id(self.template_code)
            return self.template
        elif attribute=='section':  
            self.section = self.dms.section.get_by_id(self.section_code)
            return self.section
        elif attribute in ('title', 'menu_name', 'page', 'version'):
            title     = LampadasCollection()
            menu_name = LampadasCollection()
            page      = LampadasCollection()
            version   = LampadasCollection()
            i18ns = self.dms.page_i18n.get_by_keys([['page_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                title[i18n.lang] = i18n.title
                if i18n.menu_name=='':
                    menu_name[i18n.lang] = i18n.title
                else:
                    menu_name[i18n.lang] = i18n.menu_name
                page[i18n.lang] = i18n.page
                version[i18n.lang] = i18n.version
            if attribute=='title':
                return title
            elif attribute=='menu_name':
                return menu_name
            elif attribute=='page':
                return page
            else:
                return version
        else:
            raise AttributeError('No such attribute %s' % attribute)

    def untranslated_lang_keys(self, lang):
        untranslated = []
        supported_langs = self.dms.language.get_by_keys([['supported', '=', 't']])
        for key in supported_langs.keys():
            if key not in self.title.keys():
                untranslated.append(key)
        return untranslated
