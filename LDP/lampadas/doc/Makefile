docs = Lampadas.html index.html Lampadas.xml

docs:	$(docs)

index.html:	Lampadas.xml
	xsltproc /usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/chunk.xsl Lampadas.xml

Lampadas.html:	Lampadas.xml
	xsltproc /usr/share/sgml/docbook/stylesheet/xsl/nwalsh/html/docbook.xsl Lampadas.xml > Lampadas.html
	
Lampadas.xml:	Lampadas.wt
	wt2db -a Lampadas.wt -o Lampadas.xml

clean:
	rm -f $(docs)
	rm -f *.html
