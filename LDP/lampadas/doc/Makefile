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
	rm -f $(docs)
	rm -f *.html
	rm -rf Lampadas.xml

xml:	Lampadas.xml

html:	Lampadas.html

index:	index.html

index.html:	Lampadas.xml
	xsltproc ../xsl/lampadas-html-chunk.xsl Lampadas.xml

Lampadas.html:	Lampadas.xml
	xsltproc ../xsl/lampadas-html.xsl Lampadas.xml > Lampadas.html
	
Lampadas.xml:	Lampadas.wt
	wt2db -x Lampadas.wt -o Lampadas.xml
	
preview: Lampadas.html
#	galeon Lampadas.html
	mozilla -remote "openURL(file:///home/david/ldp/cvs/LDP/lampadas/doc/Lampadas.html)"

.SUFFIXES: .sgml .1 .5

.sgml.1:
	if which docbook-to-man; then \
	  docbook-to-man $< > $@; \
        else \
	  docbook2man $<; \
        fi

.sgml.5:
	if which docbook-to-man; then \
	  docbook-to-man $< > $@; \
        else \
	  docbook2man $<; \
        fi
