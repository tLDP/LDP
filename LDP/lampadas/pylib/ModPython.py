#!/usr/bin/python

from Log import log
from HTML import page_factory
from Config import config
from URLParse import URI
from mod_python import apache
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
        send_HTML(req, page_factory.page(req.uri))
    return apache.OK


def send_HTML(req, HTML):
    """
    Send the passed HTML page.
    """
    log(3, 'Sending HTML')
    req.content_type = 'text/html'
    req.send_http_header()
    req.write(HTML)


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
    req.content_type = mimetype
    req.send_http_header()
    file_contents = fd.read()
    req.write(file_contents)


def send_Text(req, text):
    """
    Send a text message.
    """
    log(3, 'Sending text')
    req.content_type = 'text/plain'
    req.send_http_header()
    req.write(text)


if __name__ == '__main__':
    pass

