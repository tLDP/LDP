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
import time

CACHE_UNLIMITED = -1
CACHE_ADJUSTMENT_TRIGGER = 25

class Cache(LampadasCollection):

    """
    Implements a data cache for a single data manager.

    By default, all data is cached.
    """
    
    def __init__(self):
        LampadasCollection.__init__(self)
        self.size   = CACHE_UNLIMITED 
        self.hits   = 0
        self.misses = 0
        self.filled = 0

    def set_size(self, size):
        """
        Establishes the size to which the cache will grow.
        If set to 0, the cache size is unbounded.
        """
        self.size = size

    def adjust_size(self):
#        print 'Adjusting cache size'
        if self.size==CACHE_UNLIMITED: return
        if len(self) > self.size + CACHE_ADJUSTMENT_TRIGGER:
            self.filled = 1
            keys = self.sort_by('last_access')[:CACHE_ADJUSTMENT_TRIGGER]
            for key in keys:
                del self[key]

    def add(self, object):
        """Adds the object to the cache."""
#        print 'Caching object ' + str(object) + ', ' + str(object.key)
        object.last_access = time.time()
        self[object.key] = object
        self.adjust_size()

    def delete(self, object):
        """Deletes the object from the cache."""
        if self.has_key(object.key):
            del self[object.key]

    def get_by_key(self, key):
        """Returns the requested object, and updates its access time."""
        if not self.has_key(key):
            return None

        object = self[key]
        if object:
            object.last_access = time.time()
            self.hits += 1
        else:
            self.misses += 1
        return object

