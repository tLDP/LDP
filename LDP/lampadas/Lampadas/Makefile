modprefix = /usr/lib/zope/lib/python/Products
mod       = $(modprefix)/Lampadas

INSTALLDIR = install -d
INSTALLMOD = install -p -m 644

all:	build

build:	

install: all
	rm -rf $(mod)
	$(INSTALLDIR) $(mod)
	cp -rp * $(mod)

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

