ALL: html pdf

clean: 

	rm -rf openMosix-HOWTO/*.html
	rm openMosix-HOWTO.pdf

html:
	docbook2html -o openMosix-HOWTO openMosix-HOWTO.sgml
pdf:

	docbook2pdf  openMosix-HOWTO.sgml
	docbook2pdf  openMosix-HOWTO.sgml

packages: 
	tar -cvzf openMosix-HOWTO.html.tar.gz openMosix-HOWTO
	tar -cvzf openMosix-HOWTO.sgml.tar.gz *.sgml *.gif *.eps ../openMosix-FAQ/*.sgml 
	gzip openMosix-HOWTO.pdf
