logprefix = /var/log

INSTALLDIR = install -d

all:	bin pylib database www conf docs xsl

install: bin pylib www conf docs
	$(INSTALLDIR) $(logprefix)/lampadas
	cd bin; $(MAKE) install
	cd pylib; $(MAKE) install
	cd database; $(MAKE) install
	cd www; $(MAKE) install
	cd conf; $(MAKE) install
	cd doc; $(MAKE) install
	cd xsl; $(MAKE) install
	echo "Lampadas installation complete."

clean:
	cd bin; $(MAKE) clean
	cd pylib; $(MAKE) clean
	cd database; $(MAKE) clean
	cd www; $(MAKE) clean
	cd conf; $(MAKE) clean
	cd doc; $(MAKE) clean
	cd xsl; $(MAKE) clean

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

xsl:
	cd xsl; $(MAKE) all

dist:
	today=`date "+%Y-%m-%d"`; \
	pwd=`pwd`; \
	dir=`basename $$pwd`; \
	tar -C .. -X exclude -vzcf lampadas-$$today.tar.gz $$dir
