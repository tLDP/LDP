#!/bin/sh
#
# $Id$
#
# Small helper script to fix broken SGML code
#
# (P) & (C) by Peter Bieringer <pb at bieringer dot de>
#
# 20020119/PB: initial


FILE_SGML="Linux+IPv6-HOWTO.sgml"
FILE_LYX="Linux+IPv6-HOWTO.lyx"
FILE_TMP="tmp.sgml"

PROG_FIX_TABLETAG="sgmllyxtabletagfix.pl"
PROG_FIX_QUOTE="sgmllyxquotefix.pl"

if [ "$FILE_LYX" -nt "$FILE_SGML" ]; then
	echo "ERR : LyX file '$FILE_LYX' is newer than SGML file '$FILE_SGML' - forgot to export?"
	exit 1
fi

if [ -f "$FILE_TMP" ]; then
	echo "INF : Temporary file exists, remove it!"
	rm "$FILE_TMP"
fi

if [ -f "$FILE_TMP" ]; then
	echo "ERR : Ooops, temporary file still exists!"
	exit 1
fi

echo "INF : Fix SGML now"
cat "$FILE_SGML" | ./$PROG_FIX_TABLETAG | ./$PROG_FIX_QUOTE >$FILE_TMP

echo "INF : Remove old SGML file '$FILE_SGML'"
rm "$FILE_SGML"

echo "INF : Rename temporary file to '$FILE_SGML'"
mv "$FILE_TMP" "$FILE_SGML"


