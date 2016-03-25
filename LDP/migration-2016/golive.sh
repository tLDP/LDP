#! /bin/bash

set -e
set -x

squawk () { printf >&2 "%s\n" "$@"; }
abort  () { squawk "$@" ; exit 1; }

SELFNAME="$( readlink --canonicalize ${0})"
ME="${SELFNAME##*/}"  # -- basename
HERE="${SELFNAME%/*}"  # -- dirname

# -- SET THIS VARIABLE to the full path of the LDP content
#
CONTENTROOT=/home/mabrown/wip/tldp/website/html

# -- trailing slash, atypically included on PUBDIR, here
PUBDIR="${CONTENTROOT}/en/"

cd "$CONTENTROOT"

READY=yes
for D in REF FAQ LDP HOWTO; do
    if ! test -d "${D}"; then
      squawk "Could not find directory ${D}."
      READY=no
    fi
    if ! test -d "${D}.compat"; then
      squawk "Could not find directory ${D}.compat."
      READY=no
    fi
done

if test "$READY" != "yes"; then
    abort "Cowardly, refusing to throw the switch."
fi

for D in REF FAQ LDP HOWTO; do

  squawk "Activating new ${D}."

  mv -v "${D}" "old.${D}" && mv -v "${D}.compat" "${D}"

  squawk "Activated  new ${D}."

done

squawk "Done.  Success."

exit 0

# -- end of file
