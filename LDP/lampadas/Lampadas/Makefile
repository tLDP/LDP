INSTALLDIR	= install -d

###########################################################
########## ADJUST THESE TO SUIT YOUR ENVIRONMENT ##########
###########################################################

# The username and groupname who will own installed files.
USERNAME	= www-data
GROUPNAME	= www-data

# The (existing) directory under which the product will be
# installed. Otherwise known as the Zope Products directory.
dest_prefix	= /usr/lib/zope/lib/python/Products


###########################################################
###### YOU SHOULDN'T HAVE TO ADJUST ITEMS BELOW HERE ######
###########################################################

# The root directory for this product
dest_base	= $(dest_prefix)/Lampadas

# All subdirectories underneath (and relative to) the base
dest_subs	= /Extensions \
		  /cmf_types \
		  /skins \
		  /skins/lampadas_scripts \
		  /skins/lampadas_templates

# All destination directories, fully qualified
dest_dirs	= $(dest_base) $(foreach sub, $(dest_subs), $(dest_base)$(sub))

# All source directories, fully qualified
source_dirs	= . $(foreach sub, $(dest_subs), .$(sub))

# We are currently optimized for a direct-from-cvs install.
# We copy all the files, then delete the ones we don't want.

# Directories to remove
remove_dirs	= $(foreach dir, $(dest_dirs), $(dir)/CVS)

# Files to remove
remove_files	= $(dest_base)/Makefile 


###########################################################
###################### BUILD TARGETS ######################
###########################################################

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


###########################################################
########## CONVENIENCE TARGETS THAT CONTROL ZOPE ##########
###########################################################

debug:
	zopectl stop
	zopectl start -D

start:
	zopectl start

restart:
	zopectl restart

stop:
	zopectl stop

