#!/usr/bin/python

__doc__ = """
This module instantiates data managers for all database tables.
"""

import datamanager
import persistence
from datamanager.cache import CACHE_UNLIMITED

dms = datamanager.DataManagers()
dms.set_object_classes(persistence)
dms.log.cache.set_size(100)

dms.session.cache.set_size(0)

# Preload data caches
#for key in dms.keys():
#    if key <> 'log':
#        dm = dms[key]
#        dm.get_all()
