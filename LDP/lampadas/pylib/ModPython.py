#!/usr/bin/python

from Log import log
#from HTML import PageFactory
from Globals import VERSION
from Config import config
#From URLParse import URI

#from mod_python import apache

def handler(req):

    from URLParse import URI

    req.content_type = 'text/plain'
    req.send_http_header()

    uri = URI(req.uri)

    filename = config.file_dir + uri.Path + '/' + uri.Filename
    filename = filename.replace('//','/')
    log.Write(3, 'looking for file ' + filename)
    
    if os.path.isfile(filename):
        send_File(filename)

    log.Write(3, 'Sending dynamic page')
    send_HTML(P.Page(self.path))

    return apache.OK

def send_String(string):
    req.write(string_d

def send_HTML(HTML):
    """
    Send the passed HTML page.
    """
    #self.send_response(200)
    req.content_type = 'text/html'
#    self.send_header("Content-length", len(HTML))
#    self.end_headers()
    send_String(HTML)
    
def send_File(self, filename):
    """
    Send the requested file.
    """
    log.Write(3, 'Sending file ' + filename)
    temp = string.split(filename, ".")
    if len(temp) > 1:
        fileext = temp[1]
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
    filesize = os.fstat(fd.fileno())[stat.ST_SIZE]
    self.send_response(200)
    self.send_header("Content-type", mimetype)
    self.send_header("Content-length", filesize)
    self.end_headers()
    return fd

def send_Text(self, text):
    """
    Send a text message.
    """
    self.send_response(200)
    self.send_header("Content-type", "text/plain")
    self.send_header("Content-length", len(text))
    self.end_headers()
    return StringIO.StringIO(text)



if __name__ == '__main__':
    pass

