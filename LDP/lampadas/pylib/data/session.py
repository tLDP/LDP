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

from Config import config
from DataLayer import lampadas
from Sessions import sessions
from HTML import page_factory
from Log import log
from mod_python import apache
import whrandom
import string

def login(req, username, password):

    user = lampadas.users[username]
    if user and user.username==username:
        if user.password == password:
            if sessions[username] == None:
                sessions.add(username, req.connection.remote_addr[0])
    
            # establish random 20 character session_id.
            # 
            chars = string.letters + string.digits
            session_id = ''
            for x in range(20):
                session_id += whrandom.choice(chars)
            user = lampadas.users[username]
            user.session_id = session_id
            user.save()
                    
            log(3, 'setting cookie')
            req.headers_out['Set-Cookie']='lampadas=' + session_id + '; path=/; expires=Wed, 09-Nov-2030 23:59:00 GMT'
            return page_factory.page('logged_in')
        else:
            return "Wrong password"
    else:
        return "User not found"

def logout(req, username):
    sessions.delete(username)

    user = lampadas.users[username]
    user.session_id = ''
    user.save()

    log(3, 'clearing cookie')
    req.headers_out['Set-Cookie']='lampadas=foo; path=/; expires=Wed, 09-Nov-1980 23:59:00 GMT'
    return page_factory.page('logged_out')

#    req.headers_out['location'] = '/home'
#    req.status = apache.HTTP_MOVED_TEMPORARILY

