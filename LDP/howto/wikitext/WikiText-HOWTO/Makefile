#DOCBOOK_XSL=/sw/share/xml/xsl/html/docbook.xsl
#DOCBOOK_CHUNK_XSL=/sw/share/xml/xsl/html/chunk.xsl
#DOCBOOK_XSL=/usr/local/share/docbook-xsl-1.61.0/html/docbook.xsl
#DOCBOOK_CHUNK_XSL=/usr/local/share/docbook-xsl-1.61.0/html/chunk.xsl
DOCBOOK_XSL=/usr/local/share/ldp-docbook/ldp-html.xsl
DOCBOOK_CHUNK_XSL=/usr/local/share/ldp-docbook/ldp-html-chunk.xsl

build:	WikiText-HOWTO.html index.html WikiText-HOWTO.txt

WikiText-HOWTO.txt:	WikiText-HOWTO.html
	lynx --dump --nolist WikiText-HOWTO.html > WikiText-HOWTO.txt

WikiText-HOWTO.html:	WikiText-HOWTO.xml
	xsltproc -o WikiText-HOWTO.html $(DOCBOOK_XSL) WikiText-HOWTO.xml

index.html:	WikiText-HOWTO.xml
	xsltproc $(DOCBOOK_CHUNK_XSL) WikiText-HOWTO.xml

WikiText-HOWTO.xml:	WikiText-HOWTO.wt
	wt2db -x -f WikiText-HOWTO.wt -o WikiText-HOWTO.xml

test:	WikiText-HOWTO.html
	linkchecker -pdavid@ibiblio.org -Fhtml -ocolored -t10 WikiText-HOWTO.html

clean:
	rm -f *.html
	rm -f WikiText-HOWTO.xml
	rm -f WikiText-HOWTO.txt

