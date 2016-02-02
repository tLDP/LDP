all: projects-out.xml

projects-out.xml: projects-in.xml projects-docb.xsl
	xsltproc projects-docb.xsl projects-in.xml | (read xml; cat > $@)

clean:
	rm -f projects-out.xml
