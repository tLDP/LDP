#!/bin/bash

# "Delete", not-so-cunning file deletion utility.
# Usage: delete filename

if [ -z "$1" ]
then
  file=nothing
else
  file=$1
fi  
# Fetch file name (or "nothing") for deletion message.


[ ! -f "$1" ] && echo "$1 not found. Can't delete a nonexistent file."
# AND LIST, to give error message if file not present.

[ ! -f "$1" ] || ( rm -f $1; echo "$file deleted." )
# OR LIST, to delete file if present.
# ( command1 ; command2 ) is, in effect, an AND LIST variant.

# Note logic inversion above.
# AND LIST executes on true, OR LIST on false.

[ ! -z "$1" ] ||  echo "Usage: `basename $0` filename"
# OR LIST, to give error message if no command line arg (file name).

exit 0
