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

from URLParse import URI
from Config import config
from mod_python import apache
import smtplib
from CoreDM import dms

def referer_lang_ext(req):
    try:
        url = req.headers_in['referer']
    except KeyError:
        url = ''
    uri = URI(url)
    return uri.lang_ext
    
def redirect(req, url):
    req.headers_out['location'] = url
    req.status = apache.HTTP_MOVED_TEMPORARILY

def go_back(req):
    if req.headers_in.has_key('referer'):
        url = req.headers_in['referer']
    else:
        url = '/'
    redirect(req, url)

def error(message):
    return message

def send_mail(email, message):
    """
    Sends an email to the user.
    """

    server = smtplib.SMTP(config.smtp_server)
    server.set_debuglevel(1)
    server.sendmail(config.admin_email, email, message)
    server.quit()

def mailpass(req, email):
    users = dms.username.get_by_keys([['email', '=', email]])
    user = users[users.keys()[0]]
    if user:
        send_mail(email, 'Your password for Lampadas is: ' + user.password)
        redirect(req, '../../password_mailed' + referer_lang_ext(req))
    else:
        return error('User not found.')

