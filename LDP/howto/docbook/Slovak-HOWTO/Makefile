# Slovak-HOWTO
# make a single SGML file from Slovak-HOWTO sources
# with latin2 chars replaced with SGML entities


SOURCES = 	apps.sgml	\
		console.sgml	\
		gettext.sgml	\
		index.sgml	\
		intro.sgml	\
		kernel.sgml	\
		locales.sgml	\
		tricks.sgml	\
		unicode.sgml	\
		xwindow.sgml


Slovak-HOWTO.sgml: $(SOURCES)
	./Single-SGML.awk <index.sgml | ./Lat2ent.pl >Slovak-HOWTO.sgml

.PHONY: clean

clean:
	rm Slovak-HOWTO.sgml
