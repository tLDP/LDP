modprefix = /usr/lib/zope/lib/python/Products
mod       = $(modprefix)/PloneCVSFile
dtml      = $(mod)/dtml
www       = $(mod)/www
skins     = $(mod)/skins
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
	
	$(INSTALLDIR) $(skins)
	$(INSTALLMOD) skins/lampadas_templates/file_edit_form  $(skins)
	
	$(INSTALLDIR) $(ext)
	$(INSTALLMOD) ext/CMFCVSInstall.py           $(ext)

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

