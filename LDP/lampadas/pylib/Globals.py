#!/usr/bin/python
# 
# This file is part of the Lampadas Documentation System.
# 
# Copyright (c) 2000, 2001, 2002 David Merrill <david@lupercalia.net>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 
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

	if tf:
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


