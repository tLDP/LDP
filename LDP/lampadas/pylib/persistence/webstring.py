#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class WebString(Persistence):

    def __getattr__(self, attribute):
        if attribute in ('string', 'version'):
            webstring = LampadasCollection()
            version = LampadasCollection()
            i18ns = self.dms.string_i18n.get_by_keys([['string_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                webstring[i18n.lang] = i18n.string
                version[i18n.lang] = i18n.version
            if attribute=='string':
                return webstring
            else:
                return version
        else:
            raise AttributeError('No such attribute %s' % attribute)

    def untranslated_lang_keys(self, lang):
        untranslated = []
        supported_langs = self.dms.language.get_by_keys([['supported', '=', 't']])
        for key in supported_langs.keys():
            if key not in self.string.keys():
                untranslated.append(key)
        return untranslated
