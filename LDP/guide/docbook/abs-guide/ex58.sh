#!/bin/bash

# Backs up all files in current directory modified within last 24 hours
# in a "tarball" (tarred and gzipped file).

NOARGS=0
E_BADARGS=65

if [ $# = $NOARGS ]
then
  echo "Usage: `basename $0` filename"
  exit $E_BADARGS
fi  

tar cvf - `find . -mtime -1 -type f -print` > $1.tar
gzip $1.tar


# Stephane Chazelas points out that the above code will fail
# if there are too many files found
# or if any filenames contain blank characters.

# He suggests the following alternatives:
# -------------------------------------------------------------
#   find . -mtime -1 -type f -print0 | xargs -0 tar rvf "$1.tar"
#      using the GNU version of "find".

#   find . -mtime -1 -type f -exec tar rvf "$1.tar" '{}' \;
#      portable to other UNIX flavors, but much slower.


exit 0
