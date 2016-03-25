#! /bin/bash

set -e
set -x

SELFNAME="$( readlink --canonicalize ${0})"
ME="${SELFNAME##*/}"  # -- basename
HERE="${SELFNAME%/*}"  # -- dirname

{
  exec 2>&1;

  bash $HERE/migration-preparation.sh;

  bash $HERE/migration-helper.sh;

  bash $HERE/golive.sh;

} | tee logfile-$( date +%F ).log

# -- end of file
