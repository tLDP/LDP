wwwprefix = /usr/local/share

INSTALLDIR = install -d
INSTALLWWW = install -p -m 644

all:	build

build:	

install: all
	$(INSTALLDIR) $(wwwprefix)/lampadas
	$(INSTALLDIR) $(wwwprefix)/lampadas/www
	$(INSTALLDIR) $(wwwprefix)/lampadas/www/images
	$(INSTALLDIR) $(wwwprefix)/lampadas/www/css
	$(INSTALLWWW) images/*.png   $(wwwprefix)/lampadas/www/images
	$(INSTALLWWW) css/*.css $(wwwprefix)/lampadas/www/css

clean:

