#!/usr/bin/perl

"""
Lampadas web interface

Index.
"""

#from lampadas.PresentLayer import HTMLGen XXXFIXME
from cStringIO import StringIO

# No need to use cookies !
# for authentication with mod_python, see 
# http://www.modpython.org/live/mod_python-2.7.1/doc-html/hand-pub-alg-auth.html

# if user authenticated :
#     redirect to user_home
# else :
#     redirect to welcome

def welcome(req) :
    buf = StringIO()
    #HTMLGen.start_page(buf,'Welcome')
    buf.write("<h1>Welcome to the %s Lampadas System</h1>" % 'LDP')
    buf.write("<ul><li><a href='document/list'>list documents</a></li></ul>")
    #HTMLGen.end_page(buf)
    return buf.getvalue()

