#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class WebString(Persistence):

    def __getattr__(self, attribute):
        if attribute=='untranslated_lang_keys':
            untranslated = []
            supported_langs = self.dms.language.get_by_keys([['supported', '=', 't']])
            for key in supported_langs.keys():
                if key not in self.string.keys():
                    untranslated.append(key)
            return untranslated
        elif attribute=='i18n':
            self.i18n = self.dms.string_i18n.get_by_keys([['code', '=', self.code]])
            return self.i18n
        elif attribute=='version':
            version = LampadasCollection()
            for key in self.i18n.keys():
                i18n = self.i18n[key]
                version[i18n.lang] = i18n.version
            return version
        elif attribute=='string':
            string = LampadasCollection()
            for key in self.i18n.keys():
                i18n = self.i18n[key]
                string[i18n.lang] = i18n.string
            return string
        else:
            raise AttributeError('No such attribute %s' % attribute)

