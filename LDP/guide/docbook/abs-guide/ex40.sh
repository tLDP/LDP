#!/bin/bash

SPEED=2    # May use higher speed if supported.
IMAGEFILE=cdimage.iso
CONTENTSFILE=contents
DEFAULTDIR=/opt

# Script to automate burning a CDR.

# Uses Joerg Schilling's "cdrecord" package.
# (http://www.fokus.gmd.de/nthp/employees/schilling/cdrecord.html)

# If this script invoked as an ordinary user, need to suid cdrecord
# (chmod u+s /usr/bin/cdrecord, as root).

if [ -z "$1" ]
then
  IMAGE_DIRECTORY=$DEFAULTDIR
# Default directory, if not specified on command line.
else
    IMAGE_DIRECTORY=$1
fi
    
ls -lRF $IMAGE_DIRECTORY > $IMAGE_DIRECTORY/$CONTENTSFILE
# The "l" option gives a "long" file listing.
# The "R" option makes the listing recursive.
# The "F" option marks the file types (directories suffixed by a /).
echo "Creating table of contents."

mkisofs -r -o $IMAGFILE $IMAGE_DIRECTORY
echo "Creating ISO9660 file system image ($IMAGEFILE)."

cdrecord -v -isosize speed=$SPEED dev=0,0 $IMAGEFILE
echo "Burning the disk."
echo "Please be patient, this will take a while."

exit 0
