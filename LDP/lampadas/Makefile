all:	docs conf

install: docs conf
	cd doc; $(MAKE) install
	cd conf; $(MAKE) install

clean:
	cd doc; $(MAKE) clean
	cd conf; $(MAKE) clean

docs:
	cd doc; $(MAKE) all

conf:
	cd conf; $(MAKE) all

