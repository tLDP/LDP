#!/usr/bin/python

__doc__ = """
This module instantiates data managers for all database tables.
"""

import datamanager
import persistence

dms = datamanager.DataManagers()
dms.set_object_classes(persistence)

