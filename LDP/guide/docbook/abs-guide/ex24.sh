#!/bin/bash

ARGS=2
E_BADARGS=65

if [ $# -ne $ARGS ]
# Check for proper no. of command line args.
then
   echo "Usage: `basename $0` phone# text-file"
   exit $E_BADARGS
fi


if [ ! -f "$2" ]
then
  echo "File $2 is not a text file"
  exit $E_BADARGS
fi
  

# Create fax formatted files from text files.
fax make $2

for file in $(ls $2.0*)
# Concatenate the converted files.
# Uses wild card in variable list.
do
  fil="$fil $file"
done  

# Do the work.
efax -d /dev/ttyS3 -o1 -t "T$1" $fil


# As S.C. points out, the for-loop can be eliminated with
#    efax -d /dev/ttyS3 -o1 -t "T$1" $2.0*
# but it's not as instructive [grin].

exit 0
