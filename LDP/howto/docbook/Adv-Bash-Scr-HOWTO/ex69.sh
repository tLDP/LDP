#!/bin/bash

# Non-interactive use of 'vi' to edit a file.
# Emulates 'sed'.

if [ -z $1 ]
then
  echo "Usage: `basename $0` filename"
  exit 1
fi

TARGETFILE=$1

vi $TARGETFILE &lt;&lt;x23LimitStringx23
i
This is line 1 of the example file.
This is line 2 of the example file.
^[
ZZ
x23LimitStringx23

# Note that ^[ above is a literal escape
# typed by Control-V Escape

exit 0
