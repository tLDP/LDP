#!/usr/bin/python

"""
Lampadas Log Module

This module generates the system log for Lampadas.
"""

# Modules ##################################################################



# Constants

LOG_FILE = 'lampadas.log'

class Log:
	"""
	Write to the system log.
	"""

	def __init__(self):
		self.log = open(LOG_FILE, 'a+')

	def __del__(self):
		self.log.close

	def __call__(self, message):
		self.Log(message)

	def Log(self, message):
		self.log.write(message + "\n")

	def Truncate(self):
		self.log.close
		self.log = open(LOG_FILE, 'w+')
