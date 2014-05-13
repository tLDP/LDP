#!/bin/sh

# Generate all available howtos

list="Linux+IPv6-HOWTO.sgml Linux+IPv6-HOWTO.de.sgml"

for lyx in $list; do
	./generate.sh $lyx $* || exit 1
done

echo -en "\a"
