modprefix = /usr/lib/zope/lib/python/Products

INSTALLDIR = install -d
INSTALLMOD = install -p -m 644

all:	build

build:	

install: all
	rm -rf $(modprefix)/PloneCVSFile
	$(INSTALLDIR) $(modprefix)/PloneCVSFile
	$(INSTALLMOD) refresh.txt $(modprefix)/PloneCVSFile
	$(INSTALLMOD) version.txt $(modprefix)/PloneCVSFile
	$(INSTALLMOD) __init__.py $(modprefix)/PloneCVSFile
	$(INSTALLMOD) PloneCVSFile.py $(modprefix)/PloneCVSFile
	$(INSTALLMOD) OMF.py $(modprefix)/PloneCVSFile
	
	$(INSTALLDIR) $(modprefix)/PloneCVSFile/skins
	#$(INSTALLMOD) skins/* $(modprefix)/PloneCVSFile/skins
	
	$(INSTALLDIR) $(modprefix)/PloneCVSFile/www
	$(INSTALLMOD) www/fish.gif $(modprefix)/PloneCVSFile/www

	$(INSTALLDIR) $(modprefix)/PloneCVSFile/dtml
	$(INSTALLMOD) dtml/create.dtml $(modprefix)/PloneCVSFile/dtml
	$(INSTALLMOD) dtml/cvsregistry_formpart.dtml $(modprefix)/PloneCVSFile/dtml
	$(INSTALLMOD) dtml/cvssandbox_formpart.dtml $(modprefix)/PloneCVSFile/dtml
	$(INSTALLMOD) dtml/cvs.dtml $(modprefix)/PloneCVSFile/dtml
	$(INSTALLMOD) dtml/cvs_form.dtml $(modprefix)/PloneCVSFile/dtml
	$(INSTALLMOD) dtml/lampadas_cvs.dtml $(modprefix)/PloneCVSFile/dtml
	$(INSTALLMOD) dtml/lampadas_cvs_form.dtml $(modprefix)/PloneCVSFile/dtml
	$(INSTALLMOD) dtml/omf_metadata.dtml $(modprefix)/PloneCVSFile/dtml

uninstall:
	rm -rf $(modprefix)/PloneCVSFile

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

