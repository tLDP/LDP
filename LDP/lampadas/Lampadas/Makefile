INSTALLDIR	= install -d
INSTALLMOD	= install -p -m 644

# These are the username and groupname who should own
# the installed files.
USERNAME	= www-data
GROUPNAME	= www-data

dest_prefix	= /usr/lib/zope/lib/python/Products
dest_base	= $(dest_prefix)/Lampadas
dest_subs	= /Extensions /cmf_types /skins /skins/lampadas_scripts /skins/lampadas_templates

dest_dirs	= $(dest_base) $(foreach sub, $(dest_subs), $(dest_base)$(sub))
source_dirs	= $(foreach sub, $(dest_subs), .$(sub))

# This is a recursive macro, to get a list of all CVS directories
remove_dirs	= $(foreach dir, $(dest_dirs), $(dir)/CVS) \
		  $(dest_base)/www
remove_files	= $(dest_base)/Makefile 

all:	build

build:	

install: all
	$(INSTALLDIR) $(foreach dir, $(dest_dirs), $(dir))
	cp -rp ./* $(dest_base)
	rm -rf $(remove_dirs) $(remove_files)
	chown -R $(USERNAME).$(GROUPNAME) $(dest_base)

uninstall:
	rm -rf $(dest_base)

clean:
	rm -f $(foreach dir, $(source_dirs), $(dir)/*.pyc)

debug:
	zopectl stop
	zopectl start -D

start:
	zopectl start

restart:
	zopectl restart

stop:
	zopectl stop

