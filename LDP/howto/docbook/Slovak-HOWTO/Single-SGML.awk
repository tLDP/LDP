#!/bin/awk -f
#
# merge Slovak-HOWTO sgml sources into one file
# author: Jan 'judas' Tomka, Oct 13 2001
# usage: single-sgml.awk <index.sgml >Slovak-HOWTO.sgml

/ENTITY[[[:blank:]]+skhowto\.\w+/ {
	sub(/skhowto\./, "", $2)
	sub(/>/, "", $4)
	a[$2] = $4
	next
}

/&skhowto\.\w+;/ {
	gsub(/\&skhowto\.|\;/, "", $1)
	system("cat " a[$1])
	next
}

{
	print $0
}

