#!/bin/bash

# Creating a swapfile.
# This script must be run as root.

FILE=/swap
BLOCKSIZE=1024
PARAM_ERROR=73
SUCCESS=0


if [ -z "$1" ]
then
  echo "Usage: `basename $0` swapfile-size"
  # Must be at least 40 blocks.
  exit $PARAM_ERROR
fi
    
dd if=/dev/zero of=$FILE bs=$BLOCKSIZE count=$1

echo "Creating swapfile of size $1 blocks (KB)."

mkswap $FILE $1
swapon $FILE

echo "Swapfile activated."

exit $SUCCESS
