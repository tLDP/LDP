#!/bin/bash

# Backs up all files in current directory
# modified within last 24 hours
# in a tarred and gzipped file.

if [ $# = 0 ]
then
  echo "Usage: `basename $0` filename"
  exit 1
fi  

tar cvf - `find . -mtime -1 -type f -print` > $1.tar
gzip $1.tar

exit 0
