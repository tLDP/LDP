#!/usr/bin/python

"""
These base classes are used to build other Lampadas objects upon.
"""

class LampadasList:
	"""
	Base class for Lampadas list objects, which are cached in RAM
	for high performance.

	Classes based on this one emulate lists, with additional methods.
	"""

	list = []

	def __len__(self):
		return len(self.list)

	def __getitem__(self, key):
		return self.list[key]

	def __setitem__(self, key, value):
		self.list[key] = value
	
	def __delitem__(self, key):
		del self.list[key]

	def items(self):
		return self.list.items()

	def append(self, item):
		self.list.append(item)
		
	def Count(self):
		return len(self.list)


class LampadasCollection:
	"""
	Base class for Lampadas collection objects, which are cached in RAM
	for high performance.

	Classes based on this one become pseudo-dictionaries, providing
	iteration and similar methods. This is done by providing a wrapper to
	the built-in dictionary type. In Python 2.2, dictionaries will be
	subclassable, so this can be rewritten to take advantage of that.
	"""

	def __init__(self):
		self.data = {}

	def __getitem__(self, key):
		try:
			item = self.data[key]
		except KeyError:
			item = None
		return item

	def __setitem__(self, key, item):
		self.data[key] = item

	def __delitem__(self, key):
		del self.data[key]

	def keys(self):
		return self.data.keys()

	def Count(self):
		return len(self.data)


