
# ad-hoc processing Makefile, for internal use /klakier

# nice version
all:
	docbook2html PLD-Guide.xml

# validate document
valid:
	nsgmls -s PLD-Guide.xml

# draft with xslt tools
draft:
	xsltproc -o index.html /usr/share/sgml/docbook/xsl-stylesheets-1.49/html/docbook.xsl PLD-Guide.xml
