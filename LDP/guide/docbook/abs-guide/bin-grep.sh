#!/bin/bash
# Locates matching strings in a binary file.

# A "grep" replacement for binary files.
# Similar effect to "grep -a"

E_BADARGS=65
NOFILE=66

if [ $# -ne 2 ]
then
  echo "Usage: `basename $0` string filename"
  exit $E_BADARGS
fi

if [ ! -f "$2" ]
then
  echo "File \"$2\" does not exist."
  exit $NOFILE
fi  


for word in $( strings "$2" | grep "$1" )
# The "strings" command lists strings in binary files,
# then piped to "grep", which tests for desired string.
do
  echo $word
done

# As S.C. points out, the above for-loop could be replaced with the simpler
#    strings "$2" | grep "$1" | tr -s "$IFS" '[\n*]'


# Try something like  "./bin-grep mem /bin/ls"  to exercise this script.

exit 0
