logprefix = /var/log

INSTALLDIR = install -d

all:	bin pylib database www conf docs

install: bin pylib www conf docs
	$(INSTALLDIR) $(logprefix)/lampadas
	cd bin; $(MAKE) install
	cd pylib; $(MAKE) install
	cd database; $(MAKE) install
	cd www; $(MAKE) install
	cd conf; $(MAKE) install
	cd doc; $(MAKE) install

clean:
	cd bin; $(MAKE) clean
	cd pylib; $(MAKE) clean
	cd database; $(MAKE) clean
	cd www; $(MAKE) clean
	cd conf; $(MAKE) clean
	cd doc; $(MAKE) clean

bin:
	cd bin; $(MAKE) all

pylib:
	cd pylib; $(MAKE) all

database:
	cd database; $(MAKE) all

www:
	cd www; $(MAKE) all

conf:
	cd conf; $(MAKE) all

docs:
	cd doc; $(MAKE) all

