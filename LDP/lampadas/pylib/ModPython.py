#!/usr/bin/python

from Log import log
from HTML import page_factory
from Config import config
from URLParse import URI
from mod_python import apache
import Cookie
import os
import string


def handler(req):

    log(3, 'handling request: ' + req.uri)
    uri = URI(req.uri)

    filename = config.file_dir + uri.path + '/' + uri.filename
    filename = filename.replace('//','/')
    filename = filename.replace('//','/')
    filename = filename.replace('//','/')
    log(3, 'looking for file ' + filename)
    
    if os.path.isfile(filename):
        send_File(req, filename)
    else:
        log(3, 'Sending dynamic page: ' + req.uri)
        cookie = get_cookie(req.headers_in, 'lampadas')
        if cookie:
            session_id = str(cookie)
        else:
            session_id = ''
        send_HTML(req, page_factory.page(req.uri, session_id))
    return apache.OK


def get_cookie(headers_in, key):
    if headers_in.has_key('Cookie'):
        cookie = Cookie.SmartCookie(headers_in['Cookie'])
        cookie.load(headers_in['Cookie'])
        if cookie.has_key(key):
            return cookie[key].value
    return None
    
def send_HTML(req, HTML):
    """
    Send the passed HTML page.
    """
    log(3, 'Sending HTML')
    req.content_type = 'text/html'
    add_content_length(req, len(HTML))
    req.send_http_header()
    req.write(HTML)
    log(3, "HTML sent")


def send_File(req, filename):
    """
    Send a file.
    """
    log(3, 'Sending file ' + filename)
    temp = string.split(filename, ".")
    if len(temp) > 1:
        fileext = temp[1]
        log(3, 'extension is ' + temp[1])
    else:
        if os.path.isfile(filename + ".png"):
            fileext = "png"
        elif os.path.isfile(filename + ".jpeg"):
            fileext = "jpeg"
        if os.path.isfile(filename + ".jpg"):
            fileext = "jpg"
        if os.path.isfile(filename + ".gif"):
            fileext = "gif"
        if fileext:
            filename += "." + fileext

    # Determine mimetype from extension
    if fileext == "html" or fileext == "htm":
        mimetype = "text/html"
    elif fileext == "png":
        mimetype = "image/png"
    elif fileext == "gif":
        mimetype = "image/gif"
    elif fileext == "jpg" or fileext == "jpeg":
        mimetype = "image/jpeg"
    elif fileext == "css":
        mimetype = "text/css"
    else:
        mimetype = "text/plain"

    fd = open(filename, 'r')
    file_contents = fd.read()
    req.content_type = mimetype
    add_content_length(req, len(file_contents))
    req.send_http_header()
    req.write(file_contents)


def send_Text(req, text):
    """
    Send a text message.
    """
    log(3, 'Sending text')
    req.content_type = 'text/plain'
    add_content_length(req, len(text))
    req.send_http_header()
    req.write(text)

def add_content_length(req, length):
    log(3, "content-length is: " + str(length))
    req.headers_out.add('Content-length', str(length))

