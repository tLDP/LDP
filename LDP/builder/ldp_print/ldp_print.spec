#
# RPM spec file for "ldp_print".
#
%define PKG_VERSION 0.90

Name: ldp_print
Summary: Generates PDF and Postscript from HTML using LDP conventions
Version: %{PKG_VERSION}
Release: 1
Copyright: GPL
Group: Development/Tools
Source: ldp_print-%{PKG_VERSION}.tgz
# URL: http://www.tldp.org
Vendor: Greg Ferguson
Packager: David A. Wheeler <dwheeler@dwheeler.com>
Prefix: /usr/local

%description
ldp_print generates PDF and Postscript files from the single-file HTML
representation of a DocBook SGML/XML document.  ldp_print assumes that the
file was created using {open}jade using the "nochunks" option.

%prep
%setup

%build
make

%install
make install

%files
/usr/local/bin/ldp_print


