logprefix = /var/log

INSTALLDIR = install -d

all:	pylib conf docs

install: bin pylib conf docs
	$(INSTALLDIR) $(logprefix)/lampadas
	cd bin; $(MAKE) install
	cd pylib; $(MAKE) install
	cd conf; $(MAKE) install
	cd doc; $(MAKE) install

clean:
	cd bin; $(MAKE) clean
	cd pylib; $(MAKE) clean
	cd conf; $(MAKE) clean
	cd doc; $(MAKE) clean

bin:
	cd bin; $(MAKE) all

pylib:
	cd pylib; $(MAKE) all

conf:
	cd conf; $(MAKE) all

docs:
	cd doc; $(MAKE) all

