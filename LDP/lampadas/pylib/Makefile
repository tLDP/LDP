modprefix = /usr/lib/python2.1/site-packages

INSTALLDIR = install -d
INSTALLMOD = install -p -m 644

all:	build

build:	

install: all
	$(INSTALLDIR) $(modprefix)/Lampadas
	$(INSTALLMOD) *.py  $(modprefix)/Lampadas

clean:
	rm -f *.pyc

