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

from DataLayer import lampadas
from Log import log
from mod_python import apache

def document(req, doc_id, title, url, ref_url, pub_status_code, class_id,
             review_status_code, tech_review_status_code, license, pub_date,
             last_update, version, tickle_date, isbn, lang, abstract):

    if not doc_id:
        return error("A required parameter is missing. Please go back and correct the error.")

    doc = lampadas.Docs[int(doc_id)]
    if doc == None:
        return error("Cannot find document " + str(doc_id))

    doc.Title                   = title
    doc.URL                     = url
    doc.HomeURL                 = ref_url
    doc.PubStatusCode           = pub_status_code
    doc.ClassID                 = int(class_id)
    doc.ReviewStatusCode        = review_status_code
    doc.TechReviewStatusCode    = tech_review_status_code
    doc.License                 = license
    doc.PubDate                 = pub_date
    doc.LastUpdate              = last_update
    doc.Version                 = version
    doc.TickleDate              = tickle_date
    doc.ISBN                    = isbn
    doc.Lang                    = lang
    doc.Abstract                = abstract
    doc.Save()
    referer = req.headers_in['referer']
    req.headers_out['location'] = referer
    req.status = apache.HTTP_MOVED_TEMPORARILY
    return "Document saved. You are being redirected to http://www.modpython.org/"

def error(message):
    return message

