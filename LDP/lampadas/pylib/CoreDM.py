#!/usr/bin/python

__doc__ = """
This module instantiates data managers for all database tables.
"""

import datamanager
import persistence
import dataset
from datamanager.cache import CACHE_UNLIMITED

dms = datamanager.DataManagers()
dms.set_objects(persistence)
dms.set_datasets(dataset)

# Cache only 100 entries in the log.
dms.log.cache.set_size(100)

# Do not cache sessions at all.
dms.session.cache.set_size(0)
