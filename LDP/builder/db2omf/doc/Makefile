MAN_DIR = $(DESTDIR)/usr/share/man/man1
DOC_DIR = /usr/share/doc/db2omf

INSTALLDIR = install -d
INSTALLDOC = install -p -m 644

all:	build

build:	man html

man:	db2omf.1

html:	db2omf.html

db2omf.1:	db2omf.pod
	pod2man db2omf.pod db2omf.1

db2omf.html:	db2omf.pod
	pod2html --title="db2omf" db2omf.pod > db2omf.html

install:	all
	$(INSTALLDIR) $(MAN_DIR)
	$(INSTALLDOC) db2omf.1 $(MAN_DIR)/db2omf.1
	$(INSTALLDIR) $(DOC_DIR)
	$(INSTALLDOC) db2omf.html $(DOC_DIR)/db2omf.html

# Publishes the documentation on the official LDP homepage.
# This assumes you're running on an iBiblio machine and have a symlink
# to the root of the LDP site at ~/LDP.
#
publish: html
	cp -p db2omf.html /export/sunsite/users/dmerrill/LDP/db2omf/index.html

clean:
	rm -f db2omf.1
	rm -f db2omf.html
	rm -f pod2htmd.x~~
	rm -f pod2htmi.x~~
