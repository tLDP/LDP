#!/bin/bash
# symlinks.sh: Lists symbolic links in a directory.


directory=${1-`pwd`}
#  Defaults to current working directory,
#+ if not otherwise specified.
#  Equivalent to code block below.
# ----------------------------------------------------------
# ARGS=1                 # Expect one command-line argument.
#
# if [ $# -ne "$ARGS" ]  # If not 1 arg...
# then
#   directory=`pwd`      # current working directory
# else
#   directory=$1
# fi
# ----------------------------------------------------------

echo "symbolic links in directory \"$directory\""

for file in "$( find $directory -type l )"   # -type l = symbolic links
do
  echo "$file"
done | sort                                  # Otherwise file list is unsorted.

#  As Dominik 'Aeneas' Schnitzer points out,
#+ failing to quote  $( find $directory -type l )
#+ will choke on filenames with embedded whitespace.

exit 0
