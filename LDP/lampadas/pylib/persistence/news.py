#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

class News(Persistence):

    def __getattr__(self, attribute):
        if attribute in ('headline', 'news', 'version'):
            self.name = LampadasCollection()
            self.description = LampadasCollection()
            self.news = LampadasCollection()
            i18ns = self.dms.news_i18n.get_by_keys([['news_code', '=', self.code]])
            for key in i18ns.keys():
                i18n = i18ns[key]
                self.version[i18n.lang] = i18n.version
                self.headline[i18n.lang] = i18n.headline
                self.news[i18n.lang] = i18n.news
        if attribute=='version':
            return self.version
        elif attribute=='headline':
            return self.headline
        else:
            return self.news

