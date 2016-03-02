MAN_DIR = $(DESTDIR)/usr/share/man/man1
DOC_DIR = /usr/share/doc/texi2db

INSTALLDIR = install -d
INSTALLDOC = install -p -m 644

all:	build

build:	man html

man:	texi2db.1

html:	texi2db.html

texi2db.1:	texi2db.pod
	pod2man texi2db.pod texi2db.1

texi2db.html:	texi2db.pod
	pod2html --title="texi2db" texi2db.pod > texi2db.html

install:	all
	$(INSTALLDIR) $(MAN_DIR)
	$(INSTALLDOC) texi2db.1 $(MAN_DIR)/texi2db.1
	$(INSTALLDIR) $(DOC_DIR)
	$(INSTALLDOC) texi2db.html $(DOC_DIR)/texi2db.html

# Publishes the documentation on the official LDP homepage.
# This assumes you're running on an iBiblio machine and have a symlink
# to the root of the LDP site at ~/LDP.
#
publish: html
	cp -p texi2db.html /export/sunsite/users/dmerrill/LDP/texi2db/index.html

clean:
	rm -f texi2db.1
	rm -f texi2db.html
	rm -f pod2htmd.x~~
	rm -f pod2htmi.x~~
