#!/bin/bash

# Non-interactive use of 'vi' to edit a file.
# (Will not work with 'vim', for some reason.)
# Emulates 'sed'.

E_BADARGS=65

if [ -z "$1" ]
then
  echo "Usage: `basename $0` filename"
  exit $E_BADARGS
fi

TARGETFILE=$1

# Insert 2 lines in file, then save.
#--------Begin here document-----------#
vi $TARGETFILE &lt;&lt;x23LimitStringx23
i
This is line 1 of the example file.
This is line 2 of the example file.
^[
ZZ
x23LimitStringx23
#----------End here document-----------#

# Note that ^[ above is a literal escape
# typed by Control-V Escape.

exit 0
