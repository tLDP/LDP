#!/bin/bash

# Creating a swapfile.
# This script must be run as root.

ROOT_UID=0         # Root has $UID 0.
E_WRONG_USER=65    # Not root?

FILE=/swap
BLOCKSIZE=1024
MINBLOCKS=40
SUCCESS=0

if [ "$UID" -ne "$ROOT_UID" ]
then
  echo; echo "You must be root to run this script."; echo
  exit $E_WRONG_USER
fi  
  

blocks=${1:-$MINBLOCKS}          #  Set to default of 40 blocks,
                                 #+ if nothing specified on command line.
# This is the equivalent of the command block below.
# --------------------------------------------------
# if [ -n "$1" ]
# then
#   blocks=$1
# else
#   blocks=$MINBLOCKS
# fi
# --------------------------------------------------


if [ "$blocks" -lt $MINBLOCKS ]
then
  blocks=$MINBLOCKS              # Must be at least 40 blocks long.
fi  


echo "Creating swap file of size $blocks blocks (KB)."
dd if=/dev/zero of=$FILE bs=$BLOCKSIZE count=$blocks  # Zero out file.

mkswap $FILE $blocks             # Designate it a swap file.
swapon $FILE                     # Activate swap file.

echo "Swap file created and activated."

exit $SUCCESS
