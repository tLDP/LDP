#!/usr/bin/python

"""
The Globals module implements low level utility and convenience routines.
"""

# Modules

from string import strip

VERSION = '0.3-pre'

def wsq(astring):
	"""
	WSQ stands for "Wrap in Single Quotes". It accepts a string, and returns an escaped string
	suitable for submission to the database.

	For example, a string which contains an embedded quote will break the database unless it is replaced
	by two single quotes.

	This routine also replaces null strings ('') with the word "NULL", so empty strings are not stored
	into the database.
	"""
	
	if astring == None:
		return 'NULL'
	elif astring == '':
		return 'NULL'
	else:
		return "'" + astring.replace("'", "''") + "'"

def dbint(anint):
	"""
	This routine converts an integer into a format ready to be submitted to the database.
	"""
	
	if anint == None:
		temp = 'NULL'
	else:
		temp = str(anint)
	return temp

def safeint(anint):
	"""
	When loading an integer value from the database, this routine replaces NULL values with zeroes.
	"""
	
	if anint == None:
		return 0
	elif anint == '':
		return 0
	else:
		return int(anint)

def bool2tf(bool):
	"""
	Converts a 1/0 integer value into a t/f string value suitable for submission to the database.
	"""
	
	if bool == 1:
		return 't'
	else:
		return 'f'

def tf2bool(tf):
	"""
	Converts a t/f string value into a 1/0 integer value.
	"""
	
	if tf == 't':
		return 1
	else:
		return 0

def trim(astring):
	"""
	Trims leading and trailing spaces from a string.
	"""
	
	if astring == None:
		temp = ''
	else:
		temp = str(astring)
	return strip(temp)


