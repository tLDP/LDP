modprefix = /usr/lib/zope/lib/python/Products
mod       = $(modprefix)/PloneCVSFile
dtml      = $(mod)/dtml
www       = $(mod)/www
skins     = $(mod)/skins
content   = $(mod)/skins/lampadas_content/
forms     = $(mod)/skins/lampadas_forms/
templates = $(mod)/skins/lampadas_templates/
slots     = $(mod)/skins/lampadas_templates/ui_slots
ext       = $(mod)/Extensions

INSTALLDIR = install -d
INSTALLMOD = install -p -m 644

MOD = 

all:	build

build:	

install: all
	rm -rf $(modprefix)/PloneCVSFile
	$(INSTALLDIR) $(modprefix)/PloneCVSFile
	$(INSTALLMOD) __init__.py     $(mod)
	$(INSTALLMOD) Defaults.py     $(mod)
	$(INSTALLMOD) OMF.py          $(mod)
	$(INSTALLMOD) PloneCVSFile.py $(mod)
	$(INSTALLMOD) README.txt      $(mod)
	$(INSTALLMOD) refresh.txt     $(mod)
	$(INSTALLMOD) version.txt     $(mod)
	
	$(INSTALLDIR) $(dtml)
	$(INSTALLMOD) dtml/create.dtml               $(dtml)
	$(INSTALLMOD) dtml/cvs.dtml                  $(dtml)
	$(INSTALLMOD) dtml/cvs_form.dtml             $(dtml)
	$(INSTALLMOD) dtml/cvsregistry_formpart.dtml $(dtml)
	$(INSTALLMOD) dtml/cvssandbox_formpart.dtml  $(dtml)
	$(INSTALLMOD) dtml/omf_metadata.dtml         $(dtml)
	
	$(INSTALLDIR) $(www)
	$(INSTALLMOD) www/fish.gif                   $(www)
	$(INSTALLMOD) www/logo.png                   $(www)
	
	$(INSTALLDIR) $(skins)
	
	$(INSTALLDIR) $(content)
	$(INSTALLMOD) skins/lampadas_content/file_edit_form.pt $(content)
	$(INSTALLMOD) skins/lampadas_content/file_view.pt      $(content)
	
	$(INSTALLDIR) $(forms)
	$(INSTALLMOD) skins/lampadas_forms/folder_listing.pt   $(forms)
	
	$(INSTALLDIR) $(templates)
	$(INSTALLMOD) skins/lampadas_templates/header.pt       $(templates)
	$(INSTALLMOD) skins/lampadas_templates/news.pt         $(templates)
	
	$(INSTALLDIR) $(slots)
	$(INSTALLMOD) skins/lampadas_templates/ui_slots/news_slot.pt $(slots)
	
	$(INSTALLDIR) $(ext)
	$(INSTALLMOD) Extensions/CMFCVSInstall.py $(ext)

uninstall:
	rm -rf $(mod)

clean:
	rm -f *.pyc

debug:
	zopectl stop
	zopectl start -D

start:
	zopectl start

restart:
	zopectl restart

stop:
	zopectl stop

