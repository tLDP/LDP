#!/bin/bash

# Copy (verbose) all files in current directory
# to directory specified on command line.

if [ -z "$1" ]
# Exit if no argument given.
then
  echo "Usage: `basename $0` directory-to-copy-to"
  exit 65
fi  

ls . | xargs -i -t cp ./{} $1
# This is the exact equivalent of
#    cp * $1
# unless any of the filenames has "whitespace" characters.

exit 0
