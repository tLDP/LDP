#!/bin/bash

EXPECTED_ARGS=2
E_BADARGS=65

if [ $# -ne $EXPECTED_ARGS ]
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
  

fax make $2              # Create fax formatted files from text files.

for file in $(ls $2.0*)  # Concatenate the converted files.
                         # Uses wild card in variable list.
do
  fil="$fil $file"
done  

efax -d /dev/ttyS3 -o1 -t "T$1" $fil   # Do the work.


# As S.C. points out, the for-loop can be eliminated with
#    efax -d /dev/ttyS3 -o1 -t "T$1" $2.0*
# but it's not quite as instructive [grin].

exit 0
