#!/bin/bash
# zmore

#View gzipped files with 'more'

NOARGS=65
NOTFOUND=66
NOTGZIP=67

if [ $# -eq 0 ] # same effect as:  if [ -z "$1" ]
# $1 can exist, but be empty:  zmore "" arg2 arg3
then
  echo "Usage: `basename $0` filename" >&2
  # Error message to stderr.
  exit $NOARGS
  # Returns 65 as exit status of script (error code).
fi  

filename=$1

if [ ! -f "$filename" ]   # Quoting $filename allows for possible spaces.
then
  echo "File $filename not found!" >&2
  # Error message to stderr.
  exit $NOTFOUND
fi  

if [ ${filename##*.} != "gz" ]
# Using bracket in variable substitution.
then
  echo "File $1 is not a gzipped file!"
  exit $NOTGZIP
fi  

zcat $1 | more

# Uses the filter 'more.'
# May substitute 'less', if desired.


exit $?   # Script returns exit status of pipe.
# Actually "exit $?" is unnecessary, as the script will, in any case,
# return the exit status of the last command executed.
