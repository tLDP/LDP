modprefix = /usr/lib/python2.1/site-packages

INSTALLDIR = install -d
INSTALLMOD = install -p -m 644

all:	build

build:	

install: all
	$(INSTALLDIR) $(modprefix)/Lampadas
	$(INSTALLMOD) BaseClasses.py $(modprefix)/Lampadas
	$(INSTALLMOD) Config.py $(modprefix)/Lampadas
	$(INSTALLMOD) Converter.py $(modprefix)/Lampadas
	$(INSTALLMOD) DataLayer.py $(modprefix)/Lampadas
	$(INSTALLMOD) Database.py $(modprefix)/Lampadas
	$(INSTALLMOD) Globals.py $(modprefix)/Lampadas
	$(INSTALLMOD) HTML.py $(modprefix)/Lampadas
	$(INSTALLMOD) Lintadas.py $(modprefix)/Lampadas
	$(INSTALLMOD) Log.py $(modprefix)/Lampadas
	$(INSTALLMOD) URLParse.py $(modprefix)/Lampadas
	$(INSTALLMOD) WebLayer.py $(modprefix)/Lampadas

clean:
	rm -f *.pyc

