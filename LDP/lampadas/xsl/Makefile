xslprefix = /usr/local/share

INSTALLDIR = install -d
INSTALLXSL = install -p -m 644

all:	build

build:

install: all
	$(INSTALLDIR) $(xslprefix)/lampadas
	$(INSTALLDIR) $(xslprefix)/lampadas/xsl
	$(INSTALLXSL) *.xsl $(xslprefix)/lampadas/xsl

clean:

