#!/bin/sh
#
# $Id$
#
# Small helper script to copy SGML file to howto dir
#
# (P) & (C) by Peter Bieringer <pb at bieringer dot de>
#
# 20020119/PB: initial


FILE_SGML="Linux+IPv6-HOWTO.sgml"

DIRSRC="./"
DIRDST="../../howto/docbook/"

if [ ! -f "${DIRSRC}${FILE_SGML}" ]; then
	echo "ERR : Missing SGML file '${DIRSRC}${FILE_SGML}'!"
	exit 1
fi

if [ -f "${DIRDST}${FILE_SGML}" ]; then
	if [ "${DIRDST}${FILE_SGML}" -nt "${DIRSRC}${FILE_SGML}" ]; then
		echo "ERR : SGML file at destination is newer than source!"
		exit 1
	fi
fi

if [ -f "${DIRDST}${FILE_SGML}" ]; then
	echo "INF : Remove old SGML file '${DIRDST}${FILE_SGML}'"
	rm "${DIRDST}${FILE_SGML}"
fi

echo "INF : Copy new SGML file"
cp "${DIRSRC}${FILE_SGML}" "${DIRDST}${FILE_SGML}"
