#!/bin/bash
# mail-format.sh: Format e-mail messages.

# Gets rid of carets, tabs, also fold excessively long lines.

ARGS=1
E_BADARGS=65
E_NOFILE=66

if [ $# -ne $ARGS ]  # Correct number of arguments passed to script?
then
  echo "Usage: `basename $0` filename"
  exit $E_BADARGS
fi

if [ -f "$1" ]       # Check if file exists.
then
    file_name=$1
else
    echo "File \"$1\" does not exist."
    exit $E_NOFILE
fi

MAXWIDTH=70          # Width to fold long lines to.

sed '
s/^>//
s/^  *>//
s/^  *//
s/		*//
' $1 | fold -s --width=$MAXWIDTH
          # -s option to "fold" breaks lines at whitespace, if possible.

# This script was inspired by an article in a well-known trade journal
# extolling a 164K Windows utility with similar functionality.

exit 0
