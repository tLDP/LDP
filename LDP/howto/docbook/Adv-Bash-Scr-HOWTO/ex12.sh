#!/bin/bash

# This line is a comment.

filename=sys.log

if [ ! -f $filename ]
then
  touch $filename; echo "Creating file."
else
  cat /dev/null > $filename; echo "Cleaning out file."
fi  

# Of course, /var/log/messages must have
# world read permission (644) for this to work.
tail /var/log/messages > $filename  
echo "$filename contains tail end of system log."

exit 0
