all:
	rm -rf html
	mkdir -p html
	xsltproc --novalid copy.xsl ../PLD-Guide.xml | (read xml; cat) > all.xml
	xspp pld-guide.xspp > style.xsl
	cd html; xsltproc ../style.xsl ../webpage.xml
	rm -f all.xml style.xsl
	cp *.png ../figures/*.png html
	mkdir html/{figures,people}
	cp ../figures/*.png html/figures
	cp ../people/*.png html/people
	cp html/Welcome.html html/index.html
