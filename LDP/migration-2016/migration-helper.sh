#! /bin/bash

set -e
set -x

SELFNAME="$( readlink --canonicalize ${0})"
ME="${SELFNAME##*/}"  # -- basename
HERE="${SELFNAME%/*}"  # -- dirname

# -- SET THIS VARIABLE to the full path of the LDP content
#
CONTENTROOT=/home/mabrown/wip/tldp/website/html

# -- trailing slash, atypically included on PUBDIR, here
PUBDIR="${CONTENTROOT}/en/"
URL_PUBDIR=http://www.tldp.org/en/

cd "$CONTENTROOT"

# -- HOWTO handling:  build symlinks and HTTP META-EQUIV files
#
HOWTOS="${CONTENTROOT}/HOWTO/"
HOWTO_COMPAT=HOWTO.compat/
HOWTO_MIGRATOR=${HERE}/howtomigration.py

test -d "${HOWTO_COMPAT}" \
  || mkdir "${HOWTO_COMPAT}"
HOWTO_COMPAT=$( readlink --canonicalize "$HOWTO_COMPAT" )
python \
  "${HOWTO_MIGRATOR}" "${HOWTOS}" "${HOWTO_COMPAT}" "${PUBDIR}" "${URL_PUBDIR}"


# -- guide handling:  build symlinks and HTTP META-EQUIV files
#
GUIDES="${CONTENTROOT}/LDP/"
GUIDE_COMPAT=LDP.compat/
GUIDE_MIGRATOR=${HERE}/guidemigration.py

rsync --archive --verbose -- "${GUIDES}" "${GUIDE_COMPAT}"
GUIDE_COMPAT=$( readlink --canonicalize "$GUIDE_COMPAT" )
python \
  "${GUIDE_MIGRATOR}" "${GUIDES}" "${GUIDE_COMPAT}" "${PUBDIR}" "${URL_PUBDIR}"


# -- ref handling:  build symlinks and HTTP META-EQUIV files
#
REFS="${CONTENTROOT}/REF/"
REF_COMPAT=REF.compat/
REF_MIGRATOR=${HERE}/refmigration.py

rsync --archive --verbose -- "${REFS}" "${REF_COMPAT}"
REF_COMPAT=$( readlink --canonicalize "$REF_COMPAT" )
python \
  "${REF_MIGRATOR}" "${REFS}" "${REF_COMPAT}" "${PUBDIR}" "${URL_PUBDIR}"


# -- ref handling:  build symlinks and HTTP META-EQUIV files
#
FAQS="${CONTENTROOT}/FAQ/"
FAQ_COMPAT=FAQ.compat/
FAQ_MIGRATOR=${HERE}/faqmigration.py

rsync --archive --verbose -- "${FAQS}" "${FAQ_COMPAT}"
FAQ_COMPAT=$( readlink --canonicalize "$FAQ_COMPAT" )
python \
  "${FAQ_MIGRATOR}" "${FAQS}" "${FAQ_COMPAT}" "${PUBDIR}" "${URL_PUBDIR}"


exit 0

# -- end of file
