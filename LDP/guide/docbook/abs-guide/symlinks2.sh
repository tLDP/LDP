#!/bin/bash
# symlinks.sh: Lists symbolic links in a directory.

ARGS=1                 # Expect one command-line argument.
OUTFILE=symlinks.list  # save file

if [ $# -ne "$ARGS" ]  # If not 1 arg...
then
  directory=`pwd`      # current working directory
else
  directory=$1
fi

echo "symbolic links in directory \"$directory\""

for file in "$( find $directory -type l )"   # -type l = symbolic links
do
  echo "$file"
done | sort > "$OUTFILE"                     # stdout of loop
#           ^^^^^^^^^^^^                       redirected to save file.

exit 0
