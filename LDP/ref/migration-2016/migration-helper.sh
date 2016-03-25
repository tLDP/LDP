#! /bin/bash

set -e
set -x

SELFNAME="$( readlink --canonicalize ${0})"
ME="${SELFNAME##*/}"  # -- basename
DIR="${SELFNAME%/*}"  # -- dirname

HOWTO_MIGRATOR=${DIR}/howtomigration.py
GUIDE_MIGRATOR=${DIR}/guidemigration.py

CONTENTROOT=/home/mabrown/wip/tldp/website/html
cd "$CONTENTROOT"

# -- trailing slash, atypically included on PUBDIR, here
PUBDIR="${CONTENTROOT}/en/"
URL_PUBDIR=http://www.tldp.org/en/

HOWTOS="${CONTENTROOT}/HOWTO"
GUIDES="${CONTENTROOT}/LDP"

# -- HOWTO handling:  build symlinks and HTTP META-EQUIV files
#
HOWTO_COMPAT=HOWTO.compat/
test -d "${HOWTO_COMPAT}" \
  || mkdir "${HOWTO_COMPAT}"

HOWTO_COMPAT=$( readlink --canonicalize "$HOWTO_COMPAT" )

python \
  "${HOWTO_MIGRATOR}" "${HOWTOS}" "${HOWTO_COMPAT}" "${PUBDIR}" "${URL_PUBDIR}"

GUIDE_COMPAT=LDP.compat/
test -d "${GUIDE_COMPAT}" \
  || mkdir "${GUIDE_COMPAT}"

rsync --archive --verbose ./LDP/ "${GUIDE_COMPAT}/"

python \
  "${GUIDE_MIGRATOR}" "${GUIDES}" "${GUIDE_COMPAT}" "${PUBDIR}" "${URL_PUBDIR}"

exit 0

# -- end of file
