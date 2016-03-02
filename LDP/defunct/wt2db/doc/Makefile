MAN_DIR = $(DESTDIR)/usr/share/man/man1
DOC_DIR = /usr/share/doc/wt2db

INSTALLDIR = install -d
INSTALLDOC = install -p -m 644

all:	build

build:	man html

man:	wt2db.1

html:	wt2db.html

wt2db.1:	wt2db.pod
	pod2man wt2db.pod wt2db.1

wt2db.html:	wt2db.pod
	pod2html --title="wt2db" wt2db.pod > wt2db.html

install:	all
	$(INSTALLDIR) $(MAN_DIR)
	$(INSTALLDOC) wt2db.1 $(MAN_DIR)/wt2db.1
	$(INSTALLDIR) $(DOC_DIR)
	$(INSTALLDOC) wt2db.html $(DOC_DIR)/wt2db.html

# Publishes the documentation on the official LDP homepage.
# This assumes you're running on an iBiblio machine and have a symlink
# to the root of the LDP site at ~/LDP.
#
publish: html
	cp -p wt2db.html /export/sunsite/users/dmerrill/LDP/wt2db/index.html

clean:
	rm -f wt2db.1
	rm -f wt2db.html
	rm -f pod2htmd.x~~
	rm -f pod2htmi.x~~
