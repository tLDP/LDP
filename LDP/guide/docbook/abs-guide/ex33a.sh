#!/bin/bash

# Try the following when invoking this script.
#   sh ex33a -a
#   sh ex33a -abc
#   sh ex33a -a -b -c
#   sh ex33a -d
#   sh ex33a -dXYZ
#   sh ex33a -d XYZ
#   sh ex33a -abcd
#   sh ex33a -abcdZ
#   sh ex33a -z
#   sh ex33a a
# Explain the results of each of the above.

E_OPTERR=65

if [ "$#" -eq 0 ]
then   # Script needs at least one command-line argument.
  echo "Usage $0 -[options a,b,c]"
  exit $E_OPTERR
fi  

set -- `getopt "abcd:" "$@"`
# Sets positional parameters to command-line arguments.
# What happens if you use "$*" instead of "$@"?

while [ ! -z "$1" ]
do
  case "$1" in
    -a) echo "Option \"a\"";;
    -b) echo "Option \"b\"";;
    -c) echo "Option \"c\"";;
    -d) echo "Option \"d\" $2";;
     *) break;;
  esac

  shift
done

#  It is better to use the 'getopts' builtin in a script,
#+ rather than 'getopt'.
#  See "ex33.sh".

exit 0
