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


# Globals

VERSION = '0.3-cvs'


def wsq(astring):
    """
    WSQ stands for "Wrap in Single Quotes". It accepts a string,
    and delimits it with single quotes. It escapes embedded single quotes,
    returns a string suitable for inclusion in a SQL statement.

    This routine also replaces null strings ('') with the word "NULL",
    so empty strings are not stored into the database.

    FIXME: the Python DB-API 2.0 says we do not need this wsq function !
    """
    
    if astring==None:
        return 'NULL'
    elif astring=='':
        return 'NULL'
    else:
        return "'" + astring.replace("'", "''") + "'"

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
        return timestr[:19]
    else:
        return ''
        
def now_string():
    return time.strftime('%Y-%M-%d %H:%M:%S')

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
   
if __name__=='__main__':
    pass
