#!/bin/bash
# Lists symbolic links in a directory.

ARG=1  # Expect one command-line argument.

if [ $# -ne "$ARG" ]  # If not 1 arg...
then
  directory=`pwd`      # current working directory.
else
  directory=$1
fi

echo "symbolic links in directory \"$directory\""

for file in $( find $directory -type l )   # "-type l" = symbolic links
do
  echo $file
done | sort   # Otherwise file list is unsorted.

exit 0
