DOC=TimePrecision
PKG=timeprecision

STYLE=docbook-utils.dsl
#STYLE=ldp.dsl

# To be processed by xsltproc, found in libxslt package.
XSL_STYLE=titlepage.tpl

SHAREDSRC=$(STYLE) titlepage.xsl
MAINen=$(DOC).sgml
MAINpt=$(DOC).pt.sgml

.SUFFIXES: .sgml .html .pdf .ps .rtf .xsl

MAINSRC=$(MAIN) $(STYLE)


all: html
pdf: $(DOC).pdf
ps: $(DOC).ps
html: $(DOC).html
rtf: $(DOC).rtf

clean:
	rm -rf *.html *.pdf *.ps *.rtf *.tex *.out *.log *.aux *.xsl


$(DOC).html: $(MAINen) $(SHAREDSRC)



titlepage.xsl: $(XSL_STYLE)
	xsltproc -o $@ docbook/template/titlepage.xsl $(XSL_STYLE)

.sgml.html:
	xsltproc -o $@ titlepage.xsl $<

.sgml.pdf:
	jw -u -b pdf -d "$(STYLE)#print" $<
	rm *html

.sgml.ps:
	jw -u -b ps -d "$(STYLE)#print" $<
	rm *html

.sgml.rtf:
	jw -u -b rtf -d "$(STYLE)#print" $<
	rm *html

dist: clean
	if [ -z "$(ver)" ]; then \
		echo "****** Need a version to be passed. Example: \"make ver=1.3 dist\"" >&2; \
	else \
		cd ..; \
		find $(PKG) | cpio -H tar -o | gzip --best -c > $(PKG)-$(ver).tar.gz; \
	fi

publish: all
	if [ -z "$(out)" ]; then \
		echo "****** Need an output directory to be passed. Example: \"make out=../out publish\"" >&2; \
	else \
		[ ! -d $(out) ] && mkdir -p $(out); \
		cp -L $(DOC)*html *png $(out); \
		cp -L -r docbook.css images/ $(out); \
	fi
