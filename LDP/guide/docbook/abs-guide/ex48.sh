#!/bin/bash

# Copying a directory tree using cpio.

ARGS=2
E_BADARGS=65

if [ $# -ne "$ARGS" ]
then
  echo Usage: `basename $0` source destination
  exit $E_BADARGS
fi  

source=$1
destination=$2

find "$source" -depth | cpio -admvp "$destination"
# Read the man page to decipher these cpio options.

exit 0
