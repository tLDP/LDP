# a makefile for generating the Bare Metal Recovery HOW-TO

# Time-stamp: <2002-01-27 13:35:23 ccurley Makefile>

# All the scripts we incorporate into the HOWTO
# SCRIPTS = cooked/back.up.all cooked/back.up.all.ssh cooked/dev.hda cooked/get.tester cooked/make.dev.hda cooked/make.fdisk cooked/restore.all cooked/restore.all.ssh cooked/restore.metadata cooked/restore.tester cooked/save.metadata
SCRIPTS = `echo scripts/[a-z]* | sed "s/scripts\///g"`

# The base name of the document
DOCUMENT = Linux-Complete-Backup-and-Recovery-HOWTO

# The install directory. This will be mirrored to the web server
INSTALL = /home/ccurley/public_html/public/$(DOCUMENT)

# Some style sheet selections. Note the escapes for the \ and the #.
indexdsl = -d /usr/share/sgml/docbook/dsssl-stylesheets/ldp.dsl
dslhtml = -d /usr/share/sgml/docbook/dsssl-stylesheets/ldp.dsl\\\#html
dslprint = -d /usr/share/sgml/docbook/dsssl-stylesheets/ldp.dsl\\\#print


cooked:
	-mkdir cooked $(DOCUMENT) $(DOCUMENT).junk

clean:
	-rm -r $(DOCUMENT) $(DOCUMENT).[a-b]* $(DOCUMENT).[d-r]* $(DOCUMENT).[t-z]* $(DOCUMENT).smooth.html cooked ../images
	mkdir cooked $(DOCUMENT) $(DOCUMENT).junk

# scripts: $(SCRIPTS)
scripts: cooked
	for S in $(SCRIPTS) ; do \
	./buildscript $$S ; \
	done

$(DOCUMENT)/index.html: $(DOCUMENT).sgml scripts
	rm -r $(DOCUMENT).junk
	mv $(DOCUMENT) $(DOCUMENT).junk
	mkdir $(DOCUMENT)
	cd $(DOCUMENT) ; /usr/bin/jade -t sgml -i html $(indexdsl) $(dslhtml) ../$(DOCUMENT).sgml
#	cp -rp *.png $(DOCUMENT)
# 	cp -rp images $(DOCUMENT)

# this target makes is easier to type as a target name. OK, I'm lazy.
chunky: $(DOCUMENT)/index.html


$(DOCUMENT).smooth.html: $(DOCUMENT).sgml scripts
	/usr/bin/jade -V nochunks -t sgml -i html $(indexdsl) $(dslhtml) $(DOCUMENT).sgml > $(DOCUMENT).smooth.html
	cp -rp images ..
smooth: $(DOCUMENT).smooth.html

html: chunky smooth


$(DOCUMENT).rtf: $(DOCUMENT).sgml scripts
	jade -t rtf -V rtf-backend $(dslprint) $(DOCUMENT).sgml
rtf: $(DOCUMENT).rtf

$(DOCUMENT).tex: $(DOCUMENT).sgml scripts
	jade -t tex -V tex-backend $(dslprint) $(DOCUMENT).sgml
tex: $(DOCUMENT).tex

# It seems to be necessary to run this thrice in order to get the TOC
# to work correctly. I don't understand it either.

$(DOCUMENT).dvi: $(DOCUMENT).tex scripts
	jadetex $(DOCUMENT).tex
	jadetex $(DOCUMENT).tex
	jadetex $(DOCUMENT).tex

dvi: $(DOCUMENT).dvi


$(DOCUMENT).ps: $(DOCUMENT).dvi scripts
	dvips -f $(DOCUMENT).dvi -o $(DOCUMENT).ps #  -The 1.5cm,3cm ?? We don't need this, but non-US might.

ps: $(DOCUMENT).ps


# $(DOCUMENT).pdf: $(DOCUMENT).ps scripts
# 	ps2pdf $(DOCUMENT).ps

# It seems to be necessary to run this thrice in order to get the TOC
# to work correctly, and to get the TOC into to the bookmarks panel on
# the left side of the acroread reader. I don't understand it either.

$(DOCUMENT).pdf: $(DOCUMENT).tex scripts
	pdfjadetex $(DOCUMENT).tex
	pdfjadetex $(DOCUMENT).tex
	pdfjadetex $(DOCUMENT).tex

pdf: $(DOCUMENT).pdf


all: html rtf tex dvi ps pdf


ship: all
	# The chunky version for on-line viewing
	-rm -r $(INSTALL) $(INSTALL)/../images
	cp -rp $(DOCUMENT) $(INSTALL)/
	cp -rp images $(INSTALL)/..

	# PDF and PS versions for download
	cp -p  $(DOCUMENT).pdf $(DOCUMENT).ps $(INSTALL)/
	bzip2 -9 $(INSTALL)/$(DOCUMENT).ps
	bzip2 -9 $(INSTALL)/$(DOCUMENT).pdf

	# Smooth version for download
	tar -cvf $(DOCUMENT).smooth.html.tar $(DOCUMENT).smooth.html
	bzip2 -9 $(DOCUMENT).smooth.html.tar
	mv  $(DOCUMENT).smooth.html.tar.bz2 $(INSTALL)/

	# Chunky version for download
	tar -cvf $(DOCUMENT).chunky.html.tar $(DOCUMENT)
	bzip2 -9 $(DOCUMENT).chunky.html.tar
	mv $(DOCUMENT).chunky.html.tar.bz2  $(INSTALL)/

	# The source for download
	cd .. ; tar -cvf $(DOCUMENT).tar $(DOCUMENT)/README `find $(DOCUMENT)/scripts ! -name "*~" ! -type d ` $(DOCUMENT)/$(DOCUMENT).sgml $(DOCUMENT)/buildscript $(DOCUMENT)/Makefile $(DOCUMENT)/images
	cd .. ; bzip2 -9 $(DOCUMENT).tar
	cd .. ; mv $(DOCUMENT).tar.bz2  $(INSTALL)/
	ls -l $(INSTALL)

install: ship
