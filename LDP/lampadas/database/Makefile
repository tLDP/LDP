sqlprefix = /usr/local/share

INSTALLDIR = install -d
INSTALLSQL = install -p -m 644

all:	build

build:

install: all
	$(INSTALLDIR) $(sqlprefix)/lampadas
	$(INSTALLDIR) $(sqlprefix)/lampadas/sql
	$(INSTALLSQL) *.sql $(sqlprefix)/lampadas/sql

clean:

