# sgml makefile
# Scott Bronson
# 19 Dec 2001
#
# Simply run "make outputformat" where output format is one of:
#   html, html-one (one big file), ps, pdf, xml, dvi, tex, rtf, mirror
# If you run make with no arguments, it makes ALL the formats.
#   "make validate" to validate the sgml.
#   "make clean" to remove all files except for the source files
# TODO: make it recognize output files so it doesn't unnec. remake things
# 
# Benefits over compiles-sgml: doesn't re-do work, stops on all errors,
#     provides clean target.
#
# This Makefile is configured for Debian.  You need to install:
#     docbook-dsssl, jade, perl, tetex-bin


# This is the name of your document without the .sgml extension
# We will produce DOCUMENT.rtf, DOCUMENT.xml, etc.
DOCUMENT=ppp-ssh


# If you want to generate an index, use "INDEX=HTML.index".
# If not, then just comment this line out.
# INDEX=HTML.index


all: html html-one rtf xml tex mirror ps

# This creates the empty index file
index.sgml: $(DOCUMENT).sgml
	perl /usr/bin/collateindex.pl -N -o index.sgml

HTML.index: index.sgml
	jade -t sgml -V html-index -d /usr/share/sgml/docbook/stylesheet/dsssl/modular/html/docbook.dsl $(DOCUMENT).sgml
	perl /usr/bin/collateindex.pl -o index.sgml HTML.index


html: $(INDEX)
	rm -f `find . -name "*.html" -not -name $(DOCUMENT).html`
	jade -t sgml -i html -d /usr/share/sgml/docbook/stylesheet/dsssl/modular/html/docbook.dsl $(DOCUMENT).sgml

html-one: $(INDEX)
	rm -f $(DOCUMENT).html
	jade -t sgml -i html -V nochunks -d /usr/share/sgml/docbook/stylesheet/dsssl/modular/html/docbook.dsl $(DOCUMENT).sgml > $(DOCUMENT).html

rtf: $(INDEX)
	rm -f $(DOCUMENT).rtf
	jade -t rtf -V rtf-backend -d /usr/share/sgml/docbook/stylesheet/dsssl/modular/print/docbook.dsl $(DOCUMENT).sgml

# XML is broken on my system until I can find a docbook.xsl file that works.
xml: $(INDEX)
	rm -f $(DOCUMENT).xml
	jade -t sgml -i xml -d docbook.xsl $(DOCUMENT).sgml
	
tex: $(INDEX)
	rm -f $(DOCUMENT).tex $(DOCUMENT).dvi
	jade -t tex -V tex-backend -d /usr/share/sgml/docbook/stylesheet/dsssl/modular/print/docbook.dsl $(DOCUMENT).sgml
	jadetex $(DOCUMENT).tex

mirror: $(INDEX) tex
	rm -f $(DOCUMENT).mirror.ps
	dvips -h /usr/share/texmf/dvips/misc/mirr.hd -O 1.5cm,3cm -f $(DOCUMENT).dvi -o $(DOCUMENT).mirror.ps

# This was originally the following command, but "-The" kept causing errors.  dvips v. 5.86d 
# dvips -The 1.5cm,3cm -f $(DOCUMENT).dvi -o $(DOCUMENT).ps
ps: $(INDEX) tex
	rm -f $(DOCUMENT).ps
	dvips -f $(DOCUMENT).dvi -o $(DOCUMENT).ps

validate:
	nsgmls -s $(DOCUMENT).sgml

clean:
	rm -f *.htm *.html index.sgml HTML.index
	rm -f $(DOCUMENT).rtf $(DOCUMENT).xml
	rm -f $(DOCUMENT).tex $(DOCUMENT).dvi $(DOCUMENT).aux $(DOCUMENT).log
	rm -f $(DOCUMENT).ps  $(DOCUMENT).mirror.ps


