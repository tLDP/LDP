man = lampadas.1 lampadasdb.1 lampadas.conf.5
docs = Lampadas.html index.html $(man)

docprefix = /usr/doc
man1prefix = /usr/share/man/man1
man5prefix = /usr/share/man/man5

INSTALLDIR = install -d
INSTALLDOC = install -p -m 644

all:	build
build:	docs
docs:	$(docs)
man:	$(man)

install: all
	$(INSTALLDIR) $(docprefix)/lampadas
	$(INSTALLDOC) *.html $(docprefix)/lampadas
	$(INSTALLDOC) ../COPYING $(docprefix)/lampadas
	$(INSTALLDOC) ../CREDITS $(docprefix)/lampadas
	$(INSTALLDOC) ../README $(docprefix)/lampadas
	$(INSTALLDOC) lampadas.1 $(ma.1prefix)/lampadas.1
	$(INSTALLDOC) lampadasdb.1 $(ma.1prefix)/lampadasdb.1
	$(INSTALLDOC) lampadasweb.1 $(ma.1prefix)/lampadasweb.1
	$(INSTALLDOC) lampadas.conf.5 $(man5prefix)/lampadas.conf.5

clean:
	rm -f core* *~ *.html $(docs) Lampadas.xml

xml:	Lampadas.xml Lampadas.a
html:	Lampadas.html
index:	index.html

index.html:	Lampadas.xml
	xsltproc --nonet ../xsl/lampadas-html-chunk.xsl $? > $@

Lampadas.html:	Lampadas.xml
	xsltproc --nonet ../xsl/lampadas-html.xsl Lampadas.xml $? > $@
	
preview: Lampadas.html
	mozilla -remote "openURL(file://`pwd`/Lampadas.html)"
#	galeon Lampadas.html

.SUFFIXES: .xml .wt .sgml .1 .5

.wt.xml:
	wt2db -n -x $< -o $*.xml

.sgml.1:
	@if which docbook-to-man; then \
	  docbook-to-man $< > $@; \
        else \
	  docbook2man $<; \
        fi

.sgml.5:
	@if which docbook-to-man; then \
	  docbook-to-man $< > $@; \
        else \
	  docbook2man $<; \
        fi
