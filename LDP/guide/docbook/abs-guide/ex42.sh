#!/bin/bash
# copydir.sh

#  Copy (verbose) all files in current directory ($PWD)
#+ to directory specified on command line.

E_NOARGS=65

if [ -z "$1" ]   # Exit if no argument given.
then
  echo "Usage: `basename $0` directory-to-copy-to"
  exit $E_NOARGS
fi  

ls . | xargs -i -t cp ./{} $1
#            ^^ ^^      ^^
#  -t is "verbose" (output command line to stderr) option.
#  -i is "replace strings" option.
#  {} is a placeholder for output text.
#  This is similar to the use of a curly bracket pair in "find."
#
#  List the files (ls),
#+ pass the output of "ls" as arguments to "xargs" (-i -t options),
#+ then copy (cp) these arguments ({}) to new directory ($1).  
#
#  The net result is the exact equivalent of
#+   cp * $1
#+ unless any of the filenames has "whitespace" characters.

exit 0
