#!/bin/bash

# Copying a directory tree using cpio.

if [ $# -ne 2 ]
then
  echo Usage: `basename $0` source destination
  exit 1
fi  

source=$1
destination=$2

find "$source" -depth | cpio -admvp "$destination"

exit 0
