#!/bin/bash

# Format e-mail messages.
# Get rid of carets, tabs, also fold excessively long lines.

ARGS=1
E_BADARGS=65
NOFILE=66

if [ $# -ne $ARGS ]  # Check for correct number of arguments passed to script.
then
  echo "Usage: `basename $0` filename"
  exit $E_BADARGS
fi

if [ -f "$1" ]  # See if file exists.
then
    file_name=$1
else
    echo "File \"$1\" does not exist."
    exit $NOFILE
fi

WIDTH=70   # Width to fold long lines to.

sed '
s/^>//
s/^  *>//
s/^  *//
s/		*//
' $1 | fold -s --width=$WIDTH
# -s option to fold breaks lines at spaces.

# This script was inspired by an article in a trade journal
# extolling a 164K Windows utility with similar functionality.

exit 0
