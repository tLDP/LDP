#!/bin/bash
# Changes a file to all uppercase.

E_BADARGS=65

if [ -z "$1" ]  # Standard check for command line arg.
then
  echo "Usage: `basename $0` filename"
  exit $E_BADARGS
fi  

tr a-z A-Z <"$1"

# Same effect as above, but using POSIX character set notation:
#        tr '[:lower:]' '[:upper:]' <"$1"
# Thanks, S.C.

exit 0
