This is the Lampadas Documentation Management System.

Lampadas provides a set of CMF Content objects which will help you
build a website to manage and publish documentation.

First there was Zope, a powerful object database and object
publisher. It's a great platform, but a platform is not much use
without some higher level frameworks, so there came the Content
Management Framework (CMF). Some folks felt CMF was powerful
but not very polished, so there came Plone, a beautiful and
powerful application built on CMF.

And then there's Lampadas, a further enhancement of Plone,
which offers the features that are needed by large documentation
projects, who serve hundreds or even thousands of documents
in many formats. A short list of features includes:

  * CVS integration -- publish files right out of your CVS tree.
    Edit them through the web interface, then commit them into
    the CVS.
  
  * Format Agnosticism -- we try to handle all the source file
    formats we can. We add support for DocBook SGML and XML and
    for LinuxDoc SGML. We want to support other formats in the
    future.

  * Powerful Meta-data -- based on the Opensource Meta-data
    Framework (OMF) from UNC Chapel Hill. Plone is already
    using Dublin Core, upon which OMF is based, so we only
    expand the Plone Meta-data.
  
REQUIREMENTS:
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

This should install everything you need. It will register the
content objects with the portal_types tool, and scripts and
templates with portal_skins.

Good luck.

