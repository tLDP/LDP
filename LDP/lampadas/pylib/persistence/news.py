#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class News(Persistence):

    def __getattr__(self, attribute):
        if attribute=='untranslated_lang_keys':
            untranslated = []
            supported_langs = self.dms.language.get_by_keys([['supported', '=', 1]])
            for key in supported_langs.keys():
                if key not in self.headline.keys():
                    untranslated.append(key)
            return untranslated
        elif attribute=='i18n':
            self.i18n = self.dms.news_i18n.get_by_keys([['id', '=', self.id]])
            return self.i18n
        elif attribute=='headline':
            headline = LampadasCollection()
            for key in self.i18n.keys():
                i18n = self.i18n[key]
                headline[i18n.lang] = i18n.headline
            return headline
        elif attribute=='version':
            version = LampadasCollection()
            for key in self.i18n.keys():
                i18n = self.i18n[key]
                version[i18n.lang] = i18n.version
            return version
        elif attribute=='news':
            news = LampadasCollection()
            for key in self.i18n.keys():
                i18n = self.i18n[key]
                news[i18n.lang] = i18n.news
            return news
        else:
            raise AttributeError('No such attribute %s' % attribute)

