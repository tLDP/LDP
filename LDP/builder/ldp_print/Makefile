
# Makefile for ldp_print

# Do "make install" to install program.

# When updating the program, change the VERSION entry here in the makefile,
# the VERSION file, and in the ldp_print.spec file.

PREFIX=/usr/local
INSTALL=install

NAME=ldp_print
VERSION=0.90

RPM_VERSION=1
# ARCH=i386
ARCH=noarch
VERSIONEDNAME=$(NAME)-$(VERSION)
INSTALL_DIR=$(PREFIX)/bin
MAN_DIR=$(PREFIX)/share/man
MAN_DIR_MAN1=$(MAN_DIR)/man1
DOC_DIR=$(PREFIX)/share/doc/$(VERSIONEDNAME)-$(RPM_VERSION)

EXECUTABLES=ldp_print



dummy:
	echo "Type 'make install' as root to install."


install_programs:
	chmod go=rx $(EXECUTABLES)
	$(INSTALL) $(EXECUTABLES) $(INSTALL_DIR)

install_docs:

install_man:

uninstall_programs:
	cd $(INSTALL_DIR) && rm -f $(EXECUTABLES)

uninstall_docs:

uninstall_man:


install: install_programs install_docs install_man

uninstall: uninstall_programs uninstall_docs uninstall_man

clean:


# Generate the versioned .tgz file.

distribute: clean
	rm -f $(NAME)-$(VERSION).tgz
	mkdir 9temp
	cp -p [A-Za-z]* 9temp
	mv 9temp $(VERSIONEDNAME)
	rm -f $(VERSIONEDNAME)/*.tgz
	rm -f $(VERSIONEDNAME)/*.tar.gz
	rm -f $(VERSIONEDNAME)/*.rpm
	rm -f $(VERSIONEDNAME)/*.1.gz
	tar -cvf - $(VERSIONEDNAME)/* | \
	gzip --best > $(VERSIONEDNAME).tgz
	chown --reference=README $(VERSIONEDNAME).tgz
	chmod a+rX *
	rm -fr $(VERSIONEDNAME)


# To make the rpm file, "make rpm" as root.
# RPM generates "noarch" files with only a specific architecture,
# so we forceably rename it.
rpm: distribute
	cp $(VERSIONEDNAME).tgz /usr/src/redhat/SOURCES
	cp $(NAME).spec /usr/src/redhat/SPECS
	cd /usr/src/redhat/SPECS
	rpm -ba $(NAME).spec
	mv /usr/src/redhat/SRPMS/$(VERSIONEDNAME)-$(RPM_VERSION)*.src.rpm .
	# The "*" replaces $(ARCH) because it really does force an arch!!
	mv /usr/src/redhat/RPMS/*/$(VERSIONEDNAME)-$(RPM_VERSION)*.rpm $(VERSIONEDNAME)-$(RPM_VERSION).noarch.rpm
	chown --reference=README *.rpm
	chmod a+r $(VERSIONEDNAME)-$(RPM_VERSION).*.rpm


