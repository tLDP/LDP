#!/bin/bash

# Formats the source of a man page for viewing in a user directory.
# This is useful when writing man page source and you want to
# look at the intermediate results on the fly while working on it.

if [ -z $1 ]
then
  echo "Usage: `basename $0` [filename]"
    exit 1
fi

groff -Tascii -man $1 | less
# From the man page for groff.

exit 0
