#!/bin/bash
# burn-cd.sh
# Script to automate burning a CDR.


SPEED=2          # May use higher speed if your hardware supports it.
IMAGEFILE=cdimage.iso
CONTENTSFILE=contents
DEFAULTDIR=/opt  # This is the directory containing the data to be burned.
                 # Make sure it exists.

# Uses Joerg Schilling's "cdrecord" package.
# (http://www.fokus.gmd.de/nthp/employees/schilling/cdrecord.html)

#  If this script invoked as an ordinary user, need to suid cdrecord
#+ (chmod u+s /usr/bin/cdrecord, as root).

if [ -z "$1" ]
then
  IMAGE_DIRECTORY=$DEFAULTDIR
  # Default directory, if not specified on command line.
else
    IMAGE_DIRECTORY=$1
fi

# Create a "table of contents" file.
ls -lRF $IMAGE_DIRECTORY > $IMAGE_DIRECTORY/$CONTENTSFILE
# The "l" option gives a "long" file listing.
# The "R" option makes the listing recursive.
# The "F" option marks the file types (directories get a trailing /).
echo "Creating table of contents."

# Create an image file preparatory to burning it onto the CDR.
mkisofs -r -o $IMAGFILE $IMAGE_DIRECTORY
echo "Creating ISO9660 file system image ($IMAGEFILE)."

# Burn the CDR.
cdrecord -v -isosize speed=$SPEED dev=0,0 $IMAGEFILE
echo "Burning the disk."
echo "Please be patient, this will take a while."

exit 0
