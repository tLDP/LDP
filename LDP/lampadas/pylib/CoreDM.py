#!/usr/bin/python

__doc__ = """
This module instantiates data managers for all database tables.
"""

import datamanager
import persistence

dms = datamanager.DataManagers()
dms.set_object_classes(persistence)

dms.session.cache.set_cache_size(0)

# Preload data caches
#for key in dms.keys():
#    if key <> 'log':
#        dm = dms[key]
#        dm.get_all()
