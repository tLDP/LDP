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

from BaseClasses import LampadasCollection
from base import Persistence

class News(Persistence):

    def __getattr__(self, attribute):
        if attribute in ('headline', 'news', 'version'):
            self.name = LampadasCollection()
            self.description = LampadasCollection()
            self.news = LampadasCollection()
            i18ns = news_i18n.get_by_keys([['news_code', '=', self.code]])
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

