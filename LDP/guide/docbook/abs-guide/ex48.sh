#!/bin/bash

# Copying a directory tree using cpio.

ARGS=2

if [ $# -ne "$ARGS" ]
then
  echo Usage: `basename $0` source destination
  exit 65
fi  

source=$1
destination=$2

find "$source" -depth | cpio -admvp "$destination"

exit 0
