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
"""
Lampadas Statistics Module

This module generates statistical information about the Lampadas system.
"""

from Globals import *
from BaseClasses import *
from Log import log
from DataLayer import lampadas


class Stats(LampadasCollection):
    """Calculates various statistical data about the system and documents."""

    def __init__(self):
        self.calc()
        
    def reset(self):
        self.data = {}
        self['general']  = StatTable(['doc_count'])
        self['pub_status'] = StatTable()
        self['lint_time'] = StatTable()
        self['mirror_time'] = StatTable()
        self['pub_time'] = StatTable()
        self['doc_error'] = StatTable()
        self['doc_format'] = StatTable()
        self['doc_dtd'] = StatTable()
        self['doc_lang'] = StatTable()
        self['pub_doc_format'] = StatTable()
        self['pub_doc_dtd'] = StatTable()
        self['pub_doc_lang'] = StatTable()
        
    def calc(self):
        self.reset()

        # Calculate document statistics by iterating through them.
        for doc_id in lampadas.docs.keys():
            doc = lampadas.docs[doc_id]
            metadata = doc.metadata()

            # Increment document counts
            self['general'].inc('doc_count')
            self['pub_status'].inc(doc.pub_status_code)
            self['doc_format'].inc(metadata.format_code)
            self['doc_dtd'].inc(metadata.dtd_code)
            self['doc_lang'].inc(doc.lang)
            
            # Increment error counts
            for key in doc.errors.sort_by('err_id'):
                self['doc_error'].inc(key)

            # Only track stats for publishable docs
            if doc.pub_status_code=='N':

                # Track when errors were checked.
                lint_time = date2str(doc.lint_time)
                self['lint_time'].inc(lint_time)

                # Must be error-checked before mirroring.
                if doc.lint_time > '':
                    mirror_time = date2str(doc.mirror_time)
                    self['mirror_time'].inc(mirror_time)

                    # Only track publishing stats for mirrored docs
                    if doc.mirror_time > '':
                        pub_time = date2str(doc.pub_time)
                        self['pub_time'].inc(pub_time)
                        
                        if doc.pub_time > '':
                            self['doc_format'].inc(metadata.format_code)
                            self['doc_dtd'].inc(metadata.dtd_code)
                            self['doc_lang'].inc(doc.lang)


class StatTable(LampadasCollection):
    """Holds a set of statistics."""

    def __init__(self, labels=[]):
        self.data = {}
        for label in labels:
            stat = Stat(label)
            stat.sort_order = len(self.data) + 1
            self[label] = stat

    def avg(self):
        """Returns the arithmetic mean of all values in this table."""
        return self.sum/len(self)
        
    def sum(self):
        """Returns the total of all values in this table."""
        value = 0
        for key in self.keys():
            value = value + self[key].value
        return value

    def pct(self, label):
        """Returns the requested value's percentage of the total."""
        
        if self[label]==None:
            return float(0)
        return float(self[label].value)/self.sum()

    def inc(self, key):
        """
        Increments the value matching the key.
        If there is no entry to match the key, create one.
        """

        stat = self[key]
        if stat==None:
            stat = Stat(key)
            self[key] = stat
        stat.value = stat.value + 1


class Stat:
    """Holds a single statistic."""

    def __init__(self, label='', value=0):
        self.sort_order = 0
        self.label      = label
        self.value      = value


stats = Stats()

