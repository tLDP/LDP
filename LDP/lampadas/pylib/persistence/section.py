#!/usr/bin/python

from BaseClasses import LampadasCollection
from base import Persistence

from Globals import STATIC, WOStringIO, state

class Section(Persistence):

    def __init__(self, dms, dm):
        super(Section, self).__init__(dms, dm)
        self.navbox = SectionNavBox(self)

    def __getattr__(self, attribute):
        if attribute=='pages':
            return self.dms.page.get_by_keys([['section_code', '=', self.code]])
        elif attribute=='static_count':
            return self.pages.count([['only_dynamic', '=', 0]])
        elif attribute=='nonregistered_count':
            return self.pages.count([['only_registered', '=', 0]])
        elif attribute=='nonadmin_count':
            return self.pages.count([['only_admin', '=', 0]])
        elif attribute=='nonsysadmin_count':
            return self.pages.count([['only_sysadmin', '=', 0]])
        elif attribute=='i18n':
            self.i18n = self.dms.section_i18n.get_by_keys([['section_code', '=', self.code]])
            return self.i18n
        elif attribute=='name':
            name = LampadasCollection()
            for key in self.i18n.keys():
                i18n = self.i18n[key]
                name[i18n.lang] = i18n.name
            return name
        else:
            raise AttributeError('No such attribute %s' % attribute)

class SectionNavBox:

    def __init__(self, section):
        self.section = section

    def get_html(self, uri):
        box = WOStringIO('<table class="navbox"><tr><th>%s</th></tr>\n'
                         '<tr><td>' % self.section.name[uri.lang])
        for key in self.section.pages.sort_by('sort_order'):
            page = self.section.pages[key]
            if STATIC and page.only_dynamic:
                continue
            if page.only_registered and state.user==None:
                continue
            if page.only_admin and (state.user==None or state.user.admin==0):
                continue
            if page.only_sysadmin and (state.user==None or state.user.sysadmin==0):
                continue
            menu_name = page.menu_name[uri.lang]
            menu_name = menu_name.replace(' ', '&nbsp;')
            box.write('<a href="|uri.base|%s|uri.lang_ext|">%s</a><br>\n' 
                % (page.code, menu_name))
        box.write('</td></tr></table>\n')
        return box.get_value()
