#!/bin/bash

# "Delete", not-so-cunning file deletion utility.
# Usage: delete filename

E_BADARGS=65

if [ -z "$1" ]
then
  echo "Usage: `basename $0` filename"
  exit $E_BADARGS
fi  


file=$1  # Set filename.

[ ! -f "$1" ] && echo "File \"$1\" not found. \
Cowardly refusing to delete a nonexistent file."
# AND LIST, to give error message if file not present.
# Note echo message continued on to a second line with an escape.

[ ! -f "$1" ] || (rm -f $1; echo "File \"$file\" deleted.")
# OR LIST, to delete file if present.
# ( command1 ; command2 ) is, in effect, an AND LIST variant.

# Note logic inversion above.
# AND LIST executes on true, OR LIST on false.

exit 0
