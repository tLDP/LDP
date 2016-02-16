
# ad-hoc processing Makefile, for internal use /klakier

# nice version
all:
	docbook2html PLD-Guide.xml

# validate document
valid:
	nsgmls -s PLD-Guide.xml

local-valid:
	xmllint --noout --dtdvalid \
		file:///usr/share/sgml/docbook/xml-dtd-4.1.2/docbookx.dtd \
		PLD-Guide.xml
# draft with xslt tools
draft:
	SGML_CATALOG_FILES=/etc/sgml/catalog \
	xsltproc --nonet --catalogs -o index.html \
	/usr/share/sgml/docbook/xsl-stylesheets-1.49/html/docbook.xsl PLD-Guide.xml
