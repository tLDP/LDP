#!/bin/bash

if [ $# -ne 2 ]
# Check for proper no. of command line args.
then
   echo "Usage: `basename $0` phone# text-file"
   exit 1
fi


if [ ! -f $2 ]
then
  echo "File $2 is not a text file"
  exit 2
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

exit 0
