all:	pylib conf docs

install: docs conf
	cd pylib; $(MAKE) install
	cd conf; $(MAKE) install
	cd doc; $(MAKE) install

clean:
	cd pylib; $(MAKE) clean
	cd conf; $(MAKE) clean
	cd doc; $(MAKE) clean

pylib:
	cd pylib; $(MAKE) all

conf:
	cd conf; $(MAKE) all

docs:
	cd doc; $(MAKE) all

