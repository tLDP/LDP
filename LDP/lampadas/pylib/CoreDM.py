#!/usr/bin/python

__doc__ = """
This module instantiates data managers for all database tables.
"""

import datamanager
import persistence
from datamanager.cache import CACHE_UNLIMITED

dms = datamanager.DataManagers()
dms.set_objects(persistence)

# Cache only 100 entries in the log.
dms.log.cache.set_size(100)

# Do not cache sessions at all.
dms.session.cache.set_size(0)
