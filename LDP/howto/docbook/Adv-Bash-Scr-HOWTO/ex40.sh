#!/bin/bash

# Script to automate burning a CDR.

# Uses Joerg Schilling's "cdrecord" package
# (http://www.fokus.gmd.de/nthp/employees/schilling/cdrecord.html)

# If this script invoked as an ordinary user, need to suid cdrecord
# (chmod u+s /usr/bin/cdrecord, as root).

if [ -z $1 ]
then
  IMAGE_DIRECTORY=/opt
# Default directory, if not specified on command line.
else
    IMAGE_DIRECTORY=$1
fi
    
ls -lR $IMAGE_DIRECTORY > $IMAGE_DIRECTORY/contents
echo "Creating table of contents."

mkisofs -r -o cdimage.iso $IMAGE_DIRECTORY
echo "Creating ISO9660 file system image (cdimage.iso)."

cdrecord -v -isosize speed=2 dev=0,0 cdimage.iso
# Change speed parameter to speed of your burner.
echo "Burning the disk."
echo "Please be patient, this will take a while."

exit 0
