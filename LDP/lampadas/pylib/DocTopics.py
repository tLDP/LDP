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

# DocTopics

from BaseClasses import *

class DocTopics(DataCollection):
    """
    A collection object providing access to document topics.
    """

    def __init__(self):
        DataCollection.__init__(self, DocTopic,
                                 'document_topic',
                                 ['topic_code', 'doc_id'],
                                 ['created', 'updated'], [])

    def add(self, doc_id, topic_code):
        sql = 'INSERT INTO document_topic(doc_id, topic_code) VALUES (' + str(doc_id) + ', ' + wsq(topic_code) + ')'
        db.runsql(sql)
        db.commit()
        doctopic = DocTopic()
        doc.topic.doc_id = doc_id
        doctopic.topic_code = topic_code
        doctopic.load()
        self[doctopic.identifier] = doctopic
        
# FIXME: Counting on the synchronizer to kick in so other Apache instances load the
# data for the new record.
# 
#        doctopic = DocTopic()
#        doctopic.doc_id = doc_id
#        doctopic.topic_code = topic_code
#        self[doctopic.topic_code] = doctopic
        
        # FIXME: How do we know it goes into this collection?

    def clear(self):
        for key in self.keys():
            self.delete(key)
            
    def delete(self, key):
        doctopic = self[key]
        if doctopic:
            sql = 'DELETE FROM document_topic WHERE doc_id=' + str(doctopic.doc_id) + ' AND topic_code=' + wsq(doctopic.topic_code)
            db.runsql(sql)
            db.commit()
            del self[key]

class DocTopic(DataObject):
    """
    A topic for the document.
    """
    pass

doctopics = DocTopics()
doctopics.load()

