#!/bin/bash

# Formats the source of a man page for viewing in a user directory.
# This is useful when writing man page source and you want to
# look at the intermediate results on the fly while working on it.

WRONGARGS=65

if [ -z "$1" ]
then
  echo "Usage: `basename $0` [filename]"
  exit $WRONGARGS
fi

groff -Tascii -man $1 | less
# From the man page for groff.

# If the man page includes tables and/or equations,
# then the above code will barf.
# The following line can handle such cases.
#
#   gtbl < "$1" | geqn -Tlatin1 | groff -Tlatin1 -mtty-char -man
#
#   Thanks, S.C.

exit 0
