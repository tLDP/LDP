#!/usr/bin/python

"""
This module implements a data cache for a single data manager.

We instantiate a separate cache for each table in order to easily
establish different caching strategies and parameters for each
type of object.

A single cache must be shared by all applications using the database.
If multiple Apache instances are running, for example, they need to
share a data cache.
"""

from Globals import *
from BaseClasses import LampadasCollection

class Cache(LampadasCollection):

    """
    Implements a data cache for a single data manager.

    By default, all data is cached.
    """
    
    def __init__(self):
        LampadasCollection.__init__(self)
        self.cache_size = 0

    def set_cache_size(self, size):
        """
        Establishes the size to which the cache will grow.
        If set to 0, the cache size is unbounded.
        """
        self.cache_size = size

    def adjust_size(self):
#        print 'Adjusting cache size'
        if self.cache_size==0: return
        keys = self.sort_by('last_access')
        while self.count() > self.cache_size:
            key = keys[0]
            del self[key]
            keys = keys[1:]

    def add(self, object):
        """Adds the object to the cache."""
#        print 'Caching object ' + str(object) + ', ' + str(object.key)
        object.last_access = now_string()
        self[object.key] = object

    def delete(self, object):
        """Deletes the object from the cache."""
        if self.has_key(object.key):
            del self[object.key]

    def get_by_key(self, key):
        """Returns the requested object, and updates its access time."""
        object = self[key]
        if object:
            object.last_access = now_string()
        return object
