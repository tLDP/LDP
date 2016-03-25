#! /bin/bash

set -e
set -x

SELFNAME="$( readlink --canonicalize ${0})"
ME="${SELFNAME##*/}"  # -- basename
DIR="${SELFNAME%/*}"  # -- dirname

CONTENTROOT=/home/mabrown/wip/tldp/website/html
cd "$CONTENTROOT"

# -- minor cleanup of dangling or otherwise broken symlinks:
for LINK in \
  html/pub/Linux/docs/HOWTO/translations/polish/.message \
  html/pub/Linux/docs/HOWTO/translations/pl/.message \
  html/LDP/LGNET/182/184 \
  ; do

  test -L "$LINK" && rm -f "$LINK"

done

ARCHIVE=archive
test -d "${ARCHIVE}" \
  || mkdir "${ARCHIVE}"

# -- populate the archive with retired items
#
mv \
  --target-directory "${ARCHIVE}" \
  --verbose \
  -- \
    HOWTO/Netscape+Proxy.html \
    HOWTO/Sendmail+UUCP.html \
    HOWTO/GTEK-BBS-550.html \
    HOWTO/DPT-Hardware-RAID.html \
    HOWTO/Consultants-HOWTO.html \
    HOWTO/WikiText-HOWTO \
    HOWTO/Security-Quickstart-Redhat-HOWTO \

# -- and populate the really ancient crap
#
TODELETE=todelete-$( date +%F )
test -d "${TODELETE}" \
  || mkdir "${TODELETE}"

mv \
  --target-directory "${TODELETE}" \
  --verbose \
  -- \
    HOWTO/Acer-Laptop-HOWTO.html \
    HOWTO/Linux-From-Scratch-HOWTO.html \
    HOWTO/Distributions-HOWTO.html \
    HOWTO/MIPS-HOWTO.html \
    HOWTO/3Dfx-HOWTO.html \
    HOWTO/PostgreSQL-HOWTO.html \

# -- end of file
