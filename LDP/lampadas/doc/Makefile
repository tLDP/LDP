docs = Lampadas.html index.html lampadasdb.8 lampadasweb.8 lampadas.conf.5
docprefix = /usr/doc
man8prefix = /usr/share/man/man8
man5prefix = /usr/share/man/man5

INSTALLDIR = install -d
INSTALLDOC = install -p -m 644

all:	build

build:	docs

docs:	$(docs)

install: all
	$(INSTALLDIR) $(docprefix)/lampadas
	$(INSTALLDOC) *.html $(docprefix)/lampadas
	$(INSTALLDOC) ../COPYING $(docprefix)/lampadas
	$(INSTALLDOC) ../CREDITS $(docprefix)/lampadas
	$(INSTALLDOC) ../README $(docprefix)/lampadas
	$(INSTALLDOC) lampadasdb.8 $(man8prefix)/lampadasdb.8
	$(INSTALLDOC) lampadasweb.8 $(man8prefix)/lampadasweb.8
	$(INSTALLDOC) lampadas.conf.5 $(man5prefix)/lampadas.conf.5

clean:
	rm -f $(docs)
	rm -f *.html
	rm -rf Lampadas.xml

index.html:	Lampadas.xml
	xsltproc /usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/chunk.xsl Lampadas.xml

Lampadas.html:	Lampadas.xml
	xsltproc /usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/docbook.xsl Lampadas.xml > Lampadas.html
	
Lampadas.xml:	Lampadas.wt
	wt2db -a Lampadas.wt -o Lampadas.xml
	
lampadasdb.8:	lampadasdb.sgml
	docbook-to-man $< > $@

lampadasweb.8:	lampadasweb.sgml
	docbook-to-man $< > $@

lampadas.conf.5:	lampadas.conf.sgml
	docbook-to-man $< > $@

