# $Id$


VERSION = 4 (Blanka)
DATE = $(shell LC_TIME=sk date +"%e. %B %Y")


SOURCES = 	apps.sgml	\
		console.sgml	\
		gettext.sgml	\
		slovak-index.sgml	\
		intro.sgml	\
		kernel.sgml	\
		locales.sgml	\
		tricks.sgml	\
		unicode.sgml	\
		xwindow.sgml

ADD_DEPS = Makefile Lat2ent.pl Single-SGML.awk


Slovak-HOWTO.sgml: $(SOURCES) $(ADD_DEPS)
	./Single-SGML.awk <slovak-index.sgml \
	| sed -e"s/@date@/$(DATE)/g" -e"s/@version@/$(VERSION)/g" \
	| ./Lat2ent.pl >Slovak-HOWTO.sgml

.PHONY: clean

clean:
	$(RM) Slovak-HOWTO.sgml
