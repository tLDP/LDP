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

import time
import string
import whrandom
import os
import htmlentitydefs

# Globals

VERSION = '0.9.4-cvs'

# Document errors
ERR_NO_SOURCE_FILE      = 001
ERR_NO_PRIMARY_FILE     = 002
ERR_TWO_PRIMARY_FILES   = 003

# File errors
ERR_FILE_NOT_FOUND      = 101
ERR_FILE_NOT_READABLE   = 102
ERR_FILE_NOT_WRITABLE   = 103
ERR_FILE_FORMAT_UNKNOWN = 104

# Mirror errors
ERR_MIRROR_NOT_FOUND    = 201  # The source file was not found.
ERR_MIRROR_URL_RETRIEVE = 202  # A error occurred retrieving a remote file.

# Make errors
ERR_MAKE_NO_SOURCE      = 301  # A source file does not exist and has no target.
ERR_MAKE_EXIT_STATUS    = 302  # A command returned a nonzero exit (failure) code.
ERR_MAKE_STDERR         = 303  # Something was written to STDERR
ERR_MAKE_ZERO_LENGTH    = 304  # Command produced a zero-length file.
ERR_MAKE_FILTER         = 305  # An error occurred running a file through lampadas-filter.

# This will be tested in the order listed
FILEMODE_MASKS = ((0400, 'r'),
                  (0200, 'w'),
                  (0100, 'x'),
                  (0040, 'r'),
                  (0020, 'w'),
                  (0010, 'x'),
                  (0004, 'r'),
                  (0002, 'w'),
                  (0001, 'x'))


def random_string(length):
    """
    Returns a string of random alphanumeric characters.
    It is intended for password generation, although it can
    be used for other purposes as well.
    """
    
    chars = string.letters + string.digits
    password = ''
    for x in range(length):
        password += whrandom.choice(chars)
    return password


def wsq(astring):
    """
    WSQ stands for "Wrap in Single Quotes". It accepts a string,
    and delimits it with single quotes. It escapes embedded single quotes,
    returning a string suitable for inclusion in a SQL statement.

    This routine also replaces null strings ('') with the word "NULL",
    so empty strings are not stored into the database.

    FIXME: the Python DB-API 2.0 says we do not need this wsq function !
    """
    
    if astring==None:
        return 'NULL'
    elif trim(astring)=='':
        return 'NULL'
    else:
        return "'" + trim(astring.replace("'", "''")) + "'"

def dbint(anint):
    """
    This routine converts an integer into its string value,
    ready to be included in a SQL statement.
    
    If the integer passed in is really None, it returns 'NULL'.
    """
    
    if anint==None:
        temp = 'NULL'
    else:
        temp = str(anint)
    return temp

def safeint(anint):
    """
    This routine converts the passed value into an integer safely,
    which means it handles None, which returns 0.
    """
    
    if anint==None:
        return 0
    elif anint=='':
        return 0
    else:
        return int(anint)

def safestr(astring):
    """
    This routine converts the passed value into a string safely,
    which means it handles None, which returns ''.
    """
    
    if astring==None:
        return '' 
    else:
        return str(astring)

def bool2yesno(bool):
    """
    Converts an integer value into a Yes/No string.

    Uses |stryes| and |strno| for localization.

    0 returns |strno|; all nonzero values return |strno|.
    """

    if bool==0:
        return '|strno|'
    else:
        return '|stryes|'
    
def bool2tf(bool):
    """
    Converts an integer value into a t/f string value suitable
    for inclusion in a SQL string. It's for PostgreSQL, which
    stores booleans as t/f.

    0 returns f; all nonzero values return t.
    """
    
    if bool==0:
        return 'f'
    else:
        return 't'

def tf2bool(tf):
    """
    Converts a boolean value from PostgreSQL (libpq.PgBoolean)
    value into a 1/0 integer value.

    t returns 1,; anything else returns 0.
    """

    if tf:
        return 1
    else:
        return 0

def date2str(date):
    """
    Converts a date value (which contains a time of "00:00:00")
    into just its date portion.
    """

    if date:
        datestr = str(date)
        return datestr[:10]
    else:
        return ''
        
def time2str(time):
    """
    Converts a date value (which contains a time of "00:00:00")
    into an ISO representation.
    """

    if time:
        timestr = str(time)
        return timestr
    else:
        return ''

def today_string():
    return time.strftime('%Y-%m-%d')

def now_string():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def trim(astring):
    """
    Trims leading and trailing spaces from a string.

    Handles None values by returning ''.
    """
    
    if astring==None:
        temp = ''
    else:
        temp = str(astring)
    return temp.strip()

def octal2permission(filemode):
    symbolic = ''
    for mask in FILEMODE_MASKS:
        if filemode & mask[0]:
            symbolic += mask[1]
        else:
            symbolic += '-'
    return symbolic

def new_sk_seriesid():
    command = 'scrollkeeper-gen-seriesid'
    process = os.popen(command)
    sk_seriesid = process.read()
    process.close()
    return sk_seriesid

def html_encode(text):
    """Encodes all entities in the text using htmlentitydefs."""

    temp = text.replace('<', '&lt;')
    temp = temp.replace('>', '&gt;')
    temp = temp.replace('"', '&quot;')
    return temp

    temp = text;
    for entity in htmlentitydefs.entitydefs.keys():
        char = htmlentitydefs.entitydefs[entity]
        if char <> '"':
            temp = temp.replace(char, '&' + entity + ';')
    return temp

def html_decode(text):
    """Decodes all entities in the text using htmlentitydefs."""

    temp = text.replace('&lt;', '<')
    temp = temp.replace('&gt;', '>')
    temp = temp.replace('&quot;', '"')
    return temp

    temp = text;
    for entity in htmlentitydefs.entitydefs.keys():
        char = htmlentitydefs.entitydefs[entity]
        if char <> '"':
            temp = temp.relace('&' + entity + ';', char)
    return temp

def escape_tokens(text):
    return text.replace('|', '\|')
   
def string_match(text1, text2):
    """Determines if the strings match except for whitespace and line breaks, etc."""

    WHITESPACE = ('\t', '\r', '\n', ' ')

    temp1 = text1
    for char in WHITESPACE:
        temp1 = temp1.replace(char, '')
    temp2 = text2
    for char in WHITESPACE:
        temp2 = temp2.replace(char, '')
    return temp1==temp2

class WOStringIO:
    """
    Write-Only pure python extra fast buffer.

    String concatenation is kinda slow. Use class WOStringIO instead:
    
    buf = WOStringIO()
    buf.write('some piece of <HTML>')
    buf.write('some other %s' % 'variable-value')
    buf.get_value()

    N.B: same interface as StringIO.

    --nico
    """

    def __init__(self,s='') :
        self.data = [s]

    def write(self,s) :
        self.data.append(s)

    def get_value(self) :
        return ''.join(self.data)


class OddEven:
    """
    This handy little class returns the strings "odd" and "even".
    Use it to set <th class="odd|even"> tags for banded tables.

    As a side feature, it also tracks how many times it has been called,
    so you have access to a row counter while building your tables.
    """
    
    def __init__(self, value='even'):
        self.value = value
        self.row   = 0

    def get_next(self):
        self.row = self.row + 1
        if self.row % 2==0:
            self.value = 'even'
        else:
            self.value = 'odd'
        return self.value

    def get_last(self):
        return self.value

if __name__=='__main__':
    pass
