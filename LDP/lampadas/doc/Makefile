docs = Lampadas.html index.html
docprefix = /usr/doc

INSTALLDIR = install -d
INSTALLDOC = install -p -m 644

all:	build

build:	docs

docs:	$(docs)

install: docs
	$(INSTALLDIR) $(docprefix)/lampadas
	$(INSTALLDOC) *.html $(docprefix)/lampadas

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
	

