all:
	rm -rf html
	mkdir -p html
	xsltproc --novalid copy.xsl ../PLD-Guide.xml | (read xml; cat) > all.xml
	xspp pld-guide.xspp > foo.xsl
	cd html; xsltproc ../foo.xsl ../webpage.xml
	cp *.png ../*.png html
	mkdir html/{installer,people}
	cp ../installer/*.png html/installer
	cp ../people/*.png html/people
