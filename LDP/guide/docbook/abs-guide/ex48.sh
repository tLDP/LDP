#!/bin/bash

# Copying a directory tree using 'cpio.'

ARGS=2
E_BADARGS=65

if [ $# -ne "$ARGS" ]
then
  echo "Usage: `basename $0` source destination"
  exit $E_BADARGS
fi  

source=$1
destination=$2

find "$source" -depth | cpio -admvp "$destination"
#               ^^^^^         ^^^^^
# Read the 'find' and 'cpio' man page to decipher these options.

#  It may be useful to check the exit status ($?) here
#+ to see if everything worked all right.

exit 0
