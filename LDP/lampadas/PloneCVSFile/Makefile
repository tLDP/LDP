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
	
	$(INSTALLDIR) $(modprefix)/PloneCVSFile/www
	$(INSTALLMOD) www/fish.gif $(modprefix)/PloneCVSFile/www

	$(INSTALLDIR) $(modprefix)/PloneCVSFile/dtml
	$(INSTALLMOD) dtml/create.dtml $(modprefix)/PloneCVSFile/dtml
	$(INSTALLMOD) dtml/cvsregistry_formpart.dtml $(modprefix)/PloneCVSFile/dtml
	$(INSTALLMOD) dtml/cvssandbox_formpart.dtml $(modprefix)/PloneCVSFile/dtml

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

