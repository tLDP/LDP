# -- Makefile for linux IP docs; written 2002-08-09; -MAB
#
#  $Id$

.SUFFIXES:
.SUFFIXES: .xml

XSLTPROC     = /usr/bin/xsltproc
OUTDIR       = /home/mabrown/public_html

# -- DocBook paths
#
XSLFO        = /docbook/xsl/fo/docbook.xsl
PRINTDSSSL   = /docbook/dsssl/print/docbook.dsl
XMLDCL       = /docbook/dsssl/dtds/decls/xml.dcl

# -- some directories used in the production of the
#    output
#
BASE         = linux-ip
XSLCHUNK     = xsl/${BASE}-chunk.xsl
XSLNOCHUNK   = xsl/${BASE}.xsl

OUTPUT       = ${OUTDIR}/linux-ip
HTMLOUTPUT   = ${OUTPUT}/html

.PHONY: all html html-nochunk images scripts print dvi distro \
	fo tex aindex syntax

all: \
	html \
	images \
	scripts

html: aindex scripts images
	${XSLTPROC} -stringparam base.dir ${HTMLOUTPUT}/ ${XSLCHUNK} ${BASE}.xml

html-nochunk:
	${XSLTPROC}  ${XSLNOCHUNK} ${BASE}.xml > ${HTMLOUTPUT}/${BASE}.html

# -- as of 2003-02-03, FO is not used, since FOP barfs on the output
#
fo:
	${XSLTPROC} -stringparam base.dir ${HTMLOUTPUT}/ ${XSLFO} ${BASE}.xml > ${HTMLOUTPUT}/${BASE}-fo.html

dvi:    tex
	( cd ${OUTPUT} ; jadetex  ${BASE}.tex || : )
	( cd ${OUTPUT} ; jadetex  ${BASE}.tex || : )
	( cd ${OUTPUT} ; jadetex  ${BASE}.tex || : )

print:  dvi
	dvipdf ${OUTPUT}/${BASE}.dvi ${OUTPUT}/${BASE}.pdf
	dvips -o ${OUTPUT}/${BASE}.ps ${OUTPUT}/${BASE}.dvi

distro: aindex html html-nochunk print
	( cd .. ; tar --create --compress --verbose --exclude \*CVS \
          --file ${OUTPUT}/${BASE}-docbook.tar.gz ${BASE} )
	( cd ${OUTPUT} ; tar --create --compress --verbose --exclude \*CVS \
          --exclude html/linux-ip.html --file ${BASE}-chunk-html.tar.gz html )
	( cd ${OUTPUT} ; tar --create --compress --verbose --exclude \*CVS \
          --file ${BASE}-single-html.tar.gz \
          html/${BASE}.html html/images html/scripts/ )
	gzip -9cf ${OUTPUT}/${BASE}.ps > ${OUTPUT}/${BASE}.ps.gz
	gzip -9cf ${OUTPUT}/${BASE}.dvi > ${OUTPUT}/${BASE}.dvi.gz

# -- yes, this is really ugly.  I'd suggest just altering
#    the paths to your DSSSL and your xml.dcl.  This is one crufty command line.
#
tex:
	openjade  -t tex -o ${OUTPUT}/${BASE}.tex \
	-d ${PRINTDSSSL} ${XMLDCL} ${BASE}.xml

syntax:
	nsgmls -sv ${XMLDCL} ${BASE}.xml

aindex:
	test -d ${OUTPUT}       || mkdir -p ${OUTPUT}
	test -d ${HTMLOUTPUT}   || mkdir -p ${HTMLOUTPUT}
	cp ${BASE}.css ${HTMLOUTPUT}
	cp index.html ${OUTPUT}

scripts:
	rm -f scripts/${BASE}-scripts.tar.gz
	@tar --create --exclude scripts/CVS --verbose --compress \
	     --file scripts/${BASE}-scripts.tar.gz scripts/
	cp -ra scripts/ ${HTMLOUTPUT}/

images:
	cp -ra images/ ${HTMLOUTPUT}/
