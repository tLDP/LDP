#!/usr/bin/python

"""
This module implements the DataSet subclass for document collections.
"""

from Globals import *
from base import DataSet

class DocumentCollection(DataSet):

    def __getattr__(self, attribute):
        if attribute=='collections':
            dataset = DataSet(self.dms.collection)
            for key in self.keys(): 
                item = self[key]
                collection = item.collection
                dataset[collection.key] = collection
            return dataset
        elif attribute=='documents':
            dataset = self.dms.document.new_dataset()
            DataSet(self.dms)
            for key in self.keys(): 
                item = self[key]
                document = item.document
                dataset[document.key] = document
            return dataset
        else:
            raise AttributeError('No such attribute %s' % attribute)
