#!/usr/bin/python

"""
This module implements the base class upon which all the individual
data sets are built.
"""

from Globals import *
from BaseClasses import LampadasCollection

class DataSet(LampadasCollection):

    def __init__(self, dms):
        super(DataSet, self).__init__()
        self.dms = dms

    def average(self, attribute):
        """Returns the average of the requested attribute."""

        if self.count()==0:
            return 0
            
        total = 0
        for key in self.keys():
            object = self[key]
            value = getattr(object, attribute)
            total = total + value
        return total / self.count()

    def max(self, attribute):
        """
        Returns the maximum value of the requested attribute.
        
        This method only supports numeric attributes.
        Returns 0 if there are no objects in the set.
        """

        maximum = 0
        for key in self.keys():
            object = self[key]
            value = getattr(object, attribute)
            maximum = max(maximum, value)
        return maximum

    def min(self, attribute):
        """
        Returns the maximum value of the requested attribute.
        
        This method only supports numeric attributes.
        Returns 0 if there are no objects in the set.
        """

        minimum = 0
        for key in self.keys():
            object = self[key]
            value = getattr(object, attribute)
            minimum = min(minimum, value)
        return minimum

    def new(self):
        return self.dms.new()

    def save(self):
        for key in self.keys():
            self[key].save()

    def add(self, object):  
        self.dms.save(object)
        self[object.key] = object

    def delete(self, object):
        if object.in_database==0:
            return
        self.dms.delete(object)
        if self.has_key(object.key):
            del self[object.key]

    def delete_by_keys(self, filters):
        subset = self.get_subset(filters)
        for key in subset.keys():
            object = self[key]
            self.delete(object)
    
    def clear(self):
        for key in self.keys():
            object = self[key]
            self.delete(object)

    def get_subset(self, filters):
        subset = DataSet(self.dms)
        for key in self.keys():
            object = self[key]
            passes = 1
            for filter in filters:
                attribute, operator, value = filter
                my_value = getattr(object, attribute)
                if operator=='=': match = (my_value==value)
                elif operator=='>': match = (my_value > value)
                elif operator=='<': match = (my_value < value)
                else:
                    raise AttributeError('No such operator: ' + operator)
                if match==0:
                    passes = 0
                    break
            if passes:
                subset[object.key] = object
        return subset

    def count(self, filters=None):
        if filters:
            i = 0
            for key in self.keys():
                object = self[key]
                passes = 1
                for filter in filters:
                    attribute, operator, value = filter
                    my_value = getattr(object, attribute)
                    if operator=='=': match = (my_value==value)
                    elif operator=='>': match = (my_value > value)
                    elif operator=='<': match = (my_value < value)
                    else:
                        raise AttributeError('No such operator: ' + operator)
                    if match==0:
                        passes = 0
                        break
                if passes:
                    i += 1
            return i
        else:
            return super(DataSet, self).count()
