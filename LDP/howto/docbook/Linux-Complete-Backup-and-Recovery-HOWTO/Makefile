# a makefile for generating the Bare Metal Recovery HOW-TO

# Time-stamp: <2007-07-02 16:06:26 ccurley Makefile>

# All the scripts we incorporate into the HOWTO. We filter out CVS,
# which is the CVS directory, and files with ~ in them, as these are
# the RCS repository files.
SCRIPTS = `ls -d scripts/* | sed "s/scripts\///g" | grep -v CVS | grep -v \~`

# Options for jade. If I read the rather terse command line help
# correctly, this is to allow it up to 65535 errors. You should not
# need this many.
JADEOPTS = -E 65535

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
	mkdir $(DOCUMENT) $(DOCUMENT).junk

# scripts: $(SCRIPTS)
scripts: cooked
	for S in $(SCRIPTS) ; do \
	./buildscript $$S ; \
	done

$(DOCUMENT)/index.html: $(DOCUMENT).sgml scripts
	rm -r $(DOCUMENT).junk
	mv $(DOCUMENT) $(DOCUMENT).junk
	mkdir $(DOCUMENT)
	cd $(DOCUMENT) ; /usr/bin/jade $(JADEOPTS) -t sgml -i html $(indexdsl) $(dslhtml) ../$(DOCUMENT).sgml

# this target makes it easier to type as a target name. OK, I'm lazy.
chunky: $(DOCUMENT)/index.html


$(DOCUMENT).smooth.html: $(DOCUMENT).sgml scripts
	/usr/bin/jade $(JADEOPTS) -V nochunks -t sgml -i html $(indexdsl) $(dslhtml) $(DOCUMENT).sgml > $(DOCUMENT).smooth.html
	cp -rp images ..
	rm -r ../images/CVS	# don't copy the CVS directory, thank you.
smooth: $(DOCUMENT).smooth.html

html: chunky smooth

$(DOCUMENT).txt: $(DOCUMENT).smooth.html
	lynx $(DOCUMENT).smooth.html --dump --nolist > $(DOCUMENT).txt

text: $(DOCUMENT).txt

$(DOCUMENT).rtf: $(DOCUMENT).sgml scripts
	jade $(JADEOPTS) -t rtf -V rtf-backend $(dslprint) $(DOCUMENT).sgml
rtf: $(DOCUMENT).rtf

$(DOCUMENT).tex: $(DOCUMENT).sgml scripts
	jade $(JADEOPTS) -t tex -V tex-backend $(dslprint) $(DOCUMENT).sgml
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


all: html rtf tex dvi ps pdf text


ship: all
	# The chunky version for on-line viewing
	-rm -r $(INSTALL)
	mkdir $(INSTALL)
	cp -rp $(DOCUMENT)/* $(INSTALL)/
	cp -rp images $(INSTALL)/..
	rm -r $(INSTALL)/../images/CVS # Don't give out the CVS data

	# PDF PS, and text versions for download
	cp -p  $(DOCUMENT).pdf $(DOCUMENT).ps $(DOCUMENT).txt $(INSTALL)/
	bzip2 -9 $(INSTALL)/$(DOCUMENT).ps
	bzip2 -9 $(INSTALL)/$(DOCUMENT).pdf
	bzip2 -9 $(INSTALL)/$(DOCUMENT).txt

	# Smooth version for download
	cd .. ; tar -cvf $(DOCUMENT).smooth.html.tar $(DOCUMENT)/$(DOCUMENT).smooth.html images
	cd .. ; bzip2 -9 $(DOCUMENT).smooth.html.tar
	cd .. ; mv  $(DOCUMENT).smooth.html.tar.bz2 $(INSTALL)/

	# Chunky version for download
	tar -cvf $(DOCUMENT).chunky.html.tar --exclude images/CVS $(DOCUMENT) images
	bzip2 -9 $(DOCUMENT).chunky.html.tar
	mv $(DOCUMENT).chunky.html.tar.bz2  $(INSTALL)/

	# The source for download
	cd .. ; tar -cvf $(DOCUMENT).tar $(DOCUMENT)/README `find $(DOCUMENT)/scripts -name "[a-z]*" ! -name "*~" ! -type d ` $(DOCUMENT)/$(DOCUMENT).sgml $(DOCUMENT)/buildscript $(DOCUMENT)/Makefile $(DOCUMENT)/images/*.gif
	cd .. ; bzip2 -9 $(DOCUMENT).tar
	cd .. ; mv $(DOCUMENT).tar.bz2  $(INSTALL)/
	cd $(INSTALL) ; md5sum *.bz2 > md5sums
	cd $(INSTALL) ; sha1sum *.bz2 > sha1sums
	ls -l $(INSTALL)

install: ship
