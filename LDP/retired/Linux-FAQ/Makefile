#DOCBOOK_XSL=/sw/share/xml/xsl/html/docbook.xsl
#DOCBOOK_CHUNK_XSL=/sw/share/xml/xsl/html/chunk.xsl
#DOCBOOK_XSL=/usr/local/share/docbook-xsl-1.61.0/html/docbook.xsl
#DOCBOOK_CHUNK_XSL=/usr/local/share/docbook-xsl-1.61.0/html/chunk.xsl
DOCBOOK_XSL=/usr/local/share/ldp-docbook/ldp-html.xsl
DOCBOOK_CHUNK_XSL=/usr/local/share/ldp-docbook/ldp-html-chunk.xsl

build:	Linux-FAQ.html index.html Linux-FAQ.txt

Linux-FAQ.txt:	Linux-FAQ.html
	lynx --dump --nolist Linux-FAQ.html > Linux-FAQ.txt

Linux-FAQ.html:	Linux-FAQ.xml
	xsltproc -o Linux-FAQ.html $(DOCBOOK_XSL) Linux-FAQ.xml

index.html:	Linux-FAQ.xml
	xsltproc $(DOCBOOK_CHUNK_XSL) Linux-FAQ.xml

Linux-FAQ.xml:	Linux-FAQ.wt
	wt2db -x -f Linux-FAQ.wt -o Linux-FAQ.xml

test:	Linux-FAQ.html
	linkchecker -pdavid@ibiblio.org -Fhtml -ocolored -t10 Linux-FAQ.html

clean:
	rm -f *.html
	rm -f Linux-FAQ.xml
	rm -f Linux-FAQ.txt

