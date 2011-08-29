#!/bin/bash

# What are all those mysterious binaries in /usr/X11R6/bin?

DIRECTORY="/usr/X11R6/bin"
# Try also "/bin", "/usr/bin", "/usr/local/bin", etc.

for file in $DIRECTORY/*
do
  whatis `basename $file`   # Echoes info about the binary.
done

exit 0

#  Note: For this to work, you must create a "whatis" database
#+ with /usr/sbin/makewhatis.
#  You may wish to redirect output of this script, like so:
#    ./what.sh >>whatis.db
#  or view it a page at a time on stdout,
#    ./what.sh | less
