
This is Lampadas, a set of CMF Content objects which will help you
build a website to manage and publish documentation.
It works by providing a set of CMFTypes that provide the specific
functionality. These types support complete OMF meta-data.

The types are:

Lampadas Document -- a folder that understands how to process its contents.
Its contents are a set of files from the CVS tree, a rendering script, and
various outputs of the rendering script.

REQUIRES:
	Plone 1.0a4+
	CMF 1.3
	Zope 2.5.1

Optional:
	on win32: win32 extensions
	   http://starship.python.net/crew/mhammond/win32/Downloads.html

	on linux: a wvWare installer
	   http://download.sourceforge.net/wvware/


Quickstart:

Add an external method to your plone site and then click its
   test tab

   Id: LampadasInstall
   Title: Lampadas installer
   Module: Lampadas.Install
   Function: install

This should install everything you need and will also register the
content objects with the portal_types tool.

Good luck.


This README contains text from the README in the CVSTypes product.
