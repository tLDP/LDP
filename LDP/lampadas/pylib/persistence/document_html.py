#!/usr/bin/python

from Widgets import widgets
from Globals import *

class DocumentView:

    def __init__(self, document):
        self.document = document

    def get_html(self, uri):
        box = WOStringIO('<table class="box" width="100%%">' 
                         '<tr><th colspan="6">|strdocdetails|</th></tr>'
                         '<tr><td class="label">|strtitle|</td><td colspan="5">%s</td></tr>\n'
                         '<tr><td class="label">|strshort_desc|</td><td colspan="5">%s</td></tr>\n'
                         '<tr><td class="label">|strabstract|</td><td colspan="5">%s</td></tr>\n'
                         '<tr><td class="label">|strstatus|</td><td>%s</td>\n'
                         '    <td class="label">|strtype|</td><td>%s</td></tr>\n'
                         '<tr><td class="label">|strversion|</td><td>%s</td>\n'
                         '    <td class="label">|strshort_title|</td><td>%s</td></tr>\n'
                         '<tr><td class="label">|strwriting|</td><td>%s</td>\n'
                         '    <td class="label">|straccuracy|</td><td>%s</td></tr>\n'
                         '<tr><td class="label">|strpub_date|</td><td>%s</td>\n'
                         '    <td class="label">|strupdated|</td><td>%s</td></tr>\n'
                         '<tr><td class="label">|strlint_time|</td><td>%s</td>\n'
                         '    <td class="label">|strmirror_time|</td><td>%s</td></tr>\n'
                         '<tr><td class="label">|strpub_time|</td><td>%s</td>\n'
                         '    <td class="label">|strtickle_date|</td><td>%s</td></tr>\n'
                         '<tr><td class="label">|strmaintained|</td><td>%s</td>\n'
                         '    <td class="label">|strrating|</td><td>%s</td></tr>\n'
                         '<tr><td class="label">|strformat|</td><td>%s</td>\n'
                         '    <td class="label">|strdtd|</td><td>%s %s</td></tr>\n'
                         '<tr><td class="label">|strlanguage|</td><td>%s</td>\n'
                         '    <td class="label">|strmaint_wanted|</td><td>%s</td></tr>\n'
                         '<tr><td class="label">|strlicense|</td><td>%s %s</td>\n'
                         '    <td class="label">|strcopyright_holder|</td><td>%s</td></tr>\n'
                         '<tr><td class="label">|strtrans_master|</td><td colspan="3">%s</td></tr>\n'
                         '    <td class="label">|strreplacedby|</td><td colspan="3">%s</td></tr>\n'
                         '<tr><td class="label">|strisbn|</td><td>%s</td>\n'
                         '    <td class="label">|strencoding|</td><td>%s</td></tr>\n'
                         '</table>'
                         % (self.document.title,
                            self.document.short_desc,
                            self.document.abstract,
                            self.document.pub_status.name[uri.lang],
                            self.document.type.name[uri.lang],
                            self.document.version,
                            self.document.short_title,
                            self.document.review_status.name[uri.lang],
                            self.document.tech_review_status.name[uri.lang],
                            self.document.pub_date, self.document.last_update,
                            self.document.lint_time, self.document.mirror_time, self.document.pub_time,
                            self.document.tickle_date,
                            bool2yesno(self.document.maintained),
                            widgets.bar_graph(self.document.rating, 10, uri.lang),
                            self.document.format.name[uri.lang],
                            self.document.dtd.name[uri.lang],
                            self.document.dtd_version,
                            self.document.language.name[uri.lang],
                            widgets.tf('maintainer_wanted', self.document.maintainer_wanted, view=1),
                            self.document.license.name[uri.lang],
                            self.document.license_version,
                            self.document.copyright_holder,
                            widgets.sk_seriesid(self.document.sk_seriesid, view=1),
                            widgets.replaced_by_id(self.document.replaced_by_id, view=1),
                            self.document.isbn,
                            self.document.encoding))
        return box.get_value()

class DocumentEdit:

    def __init__(self, document):
        self.document = document

    def get_html(self, uri):
        if (state.session==None or state.user.can_edit(doc_id=self.document.id)==0):
            return '|blknopermission|'

        box = WOStringIO('<table class="box" width="100%">' 
                         '<tr><th colspan="6">|strdocdetails|</th></tr>')
                
        if self.document.id > 0:
            #lintadas.check_doc(uri.id)
            delete_widget = widgets.delete() + '|strdelete| '
            box.write('<form method="GET" action="|uri.base|data/save/document" '
                      'name="document">')
        else:

            delete_widget = ''
            box.write('<form method="GET" action="|uri.base|data/save/newdocument" '
                      'name="document">')

        box.write('<input name="username" type="hidden" value="%s">\n'
                  '<input name="doc_id" type="hidden" value="%s">\n'
                  '<tr><td class="label">|strtitle|</td><td colspan="5">%s</td></tr>\n'
                  '<tr><td class="label">|strshort_desc|</td><td colspan="5">%s</td></tr>\n'
                  '<tr><td class="label">|strabstract|</td><td colspan="5">%s</td></tr>\n'
                  '<tr><td class="label">|strstatus|</td><td>%s</td>\n'
                  '    <td class="label">|strtype|</td><td>%s</td></tr>\n'
                  '<tr><td class="label">|strversion|</td><td>%s</td>\n'
                  '    <td class="label">|strshort_title|</td><td>%s</td></tr>\n'
                  '<tr><td class="label">|strwriting|</td><td>%s</td>\n'
                  '    <td class="label">|straccuracy|</td><td>%s</td></tr>\n'
                  '<tr><td class="label">|strpub_date|</td><td>%s</td>\n'
                  '    <td class="label">|strupdated|</td><td>%s</td></tr>\n'
                  '<tr><td class="label">|strlint_time|</td><td>%s</td>\n'
                  '    <td class="label">|strmirror_time|</td><td>%s</td></tr>\n'
                  '<tr><td class="label">|strpub_time|</td><td>%s</td>\n'
                  '    <td class="label">|strtickle_date|</td><td>%s</td></tr>\n'
                  '<tr><td class="label">|strmaintained|</td><td>%s</td>\n'
                  '    <td class="label">|strrating|</td><td>%s</td></tr>\n'
                  '<tr><td class="label">|strformat|</td><td>%s</td>\n'
                  '    <td class="label">|strdtd|</td><td>%s %s</td></tr>\n'
                  '<tr><td class="label">|strlanguage|</td><td>%s</td>\n'
                  '    <td class="label">|strmaint_wanted|</td><td>%s</td></tr>\n'
                  '<tr><td class="label">|strlicense|</td><td>%s %s</td>\n'
                  '    <td class="label">|strcopyright_holder|</td><td>%s</td></tr>\n'
                  '<tr><td class="label">|strtrans_master|</td><td colspan="3">%s</td></tr>\n'
                  '    <td class="label">|strreplacedby|</td><td colspan="3">%s</td></tr>\n'
                  '<tr><td class="label">|strisbn|</td><td>%s</td>\n'
                  '    <td class="label">|strencoding|</td><td>%s</td></tr>\n'
                  '<tr><td></td><td>%s%s</td></tr>'
                  '</table></form>'
                  % (state.user.username, self.document.id,
                     widgets.title(self.document.title),
                     widgets.short_desc(self.document.short_desc),
                     widgets.abstract(self.document.abstract),
                     widgets.pub_status_code(self.document.pub_status_code, uri.lang),
                     widgets.type_code(self.document.type_code, uri.lang),
                     widgets.version(self.document.version),
                     widgets.short_title(self.document.short_title),
                     widgets.review_status_code(self.document.review_status_code, uri.lang), 
                     widgets.tech_review_status_code(self.document.tech_review_status_code, uri.lang),
                     widgets.pub_date(self.document.pub_date), widgets.last_update(self.document.last_update),
                     widgets.lint_time(self.document.lint_time), widgets.mirror_time(self.document.mirror_time), widgets.pub_time(self.document.pub_time),
                     widgets.tickle_date(self.document.tickle_date),
                     bool2yesno(self.document.maintained),
                     widgets.bar_graph(self.document.rating, 10, uri.lang),
                     widgets.format_code(self.document.format_code, uri.lang),
                     widgets.dtd_code(self.document.dtd_code, uri.lang),
                     widgets.dtd_version(self.document.dtd_version),
                     widgets.lang(self.document.lang, uri.lang),
                     widgets.tf('maintainer_wanted', self.document.maintainer_wanted),
                     widgets.license_code(self.document.license_code, uri.lang),
                     widgets.license_version(self.document.license_version),
                     widgets.copyright_holder(self.document.copyright_holder),
                     widgets.sk_seriesid(self.document.sk_seriesid),
                     widgets.replaced_by_id(self.document.replaced_by_id),
                     widgets.isbn(self.document.isbn),
                     widgets.encoding(self.document.encoding),
                     delete_widget, widgets.save()))
        return box.get_value()
