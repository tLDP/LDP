DOC=HighQuality
PKG=highquality

STYLE=docbook-utils.dsl
#STYLE=ldp.dsl

# To be processed by xsltproc, found in libxslt package.
XSL_STYLE=titlepage.tpl

SHAREDSRC=articleinfo.sgml conffile.sgml initd.sgml rc3d.sgml service.sgml chkconfig.sgml externalconf.sgml initscript.sgml nomethod.sgml rlevelchange.sgml manysouls.sgml $(STYLE) titlepage.xsl
MAINen=$(DOC).sgml
MAINpt=$(DOC).pt.sgml

.SUFFIXES: .sgml .html .pdf .ps .rtf .xsl

MAINSRC=$(MAIN) $(STYLE)


all: html
pdf: $(DOC).pdf $(DOC).pt.pdf
ps: $(DOC).ps $(DOC).pt.ps
html: $(DOC).html $(DOC).pt.html
rtf: $(DOC).rtf $(DOC).pt.rtf

clean:
	rm -rf *.html *.pdf *.ps *.rtf *.tex *.out *.log *.aux *.xsl


$(DOC).html: $(MAINen) $(SHAREDSRC)
$(DOC).pt.html: $(MAINpt) $(SHAREDSRC)



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
		cp -L $(DOC)*html $(out); \
		cp -L -r docbook.css images/ $(out); \
	fi