#/usr/bin/python
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

from BaseClasses import *
from Docs import docs
from Languages import languages
from DocTopics import doctopics, DocTopics

# Topics

class Topics(DataCollection):
    """
    A collection object of all topics.
    """
    
    def __init__(self):
        DataCollection.__init__(self, Topic,
                               'topic',
                               {'topic_code': 'code'},
                               ['sort_order', 'parent_code'],
                               {'topic_name': 'name', 'topic_desc': 'description'})
        

    def load(self):
        DataCollection.load(self)
        self.calc_titles()

    def calc_titles(self):
        for topic_code in self.sort_by('sort_order'):
            topic = self[topic_code]
            topic.title = LampadasCollection()
            parent_code = topic.parent_code
            for lang in languages.supported_keys('EN'):
                topic.title[lang] = ''
                if parent_code > '':
                    topic.title[lang] = self[parent_code].title[lang] + ': '
                topic.title[lang] = topic.title[lang] + topic.name[lang]
    
class Topic(DataObject):
    """
    Each document can be assigned an arbitrary number of topics.
    The web interface allows a user to browse through document topics,
    to help them find a document on the subject in which they are interested.
    """

    def load_row(self, row):
        DataObject.load_row(self, row)
        self.docs = doctopics.apply_filter(DocTopics, Filter('topic_code', '=', self.code))

topics = Topics()
topics.load()
