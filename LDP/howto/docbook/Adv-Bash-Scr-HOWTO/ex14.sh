#!/bin/bash

#View gzipped files with 'most'

NOARGS=1

if [ $# = 0 ]
# same effect as:  if [ -z $1 ]
then
  echo "Usage: `basename $0` filename" >&2
  # Error message to stderr.
  exit $NOARGS
  # Returns 1 as exit status of script
  # (error code)
fi  

filename=$1

if [ ! -f $filename ]
then
  echo "File $filename not found!" >&2
  # Error message to stderr.
  exit 2
fi  

if [ ${filename##*.} != "gz" ]
# Using bracket in variable substitution.
then
  echo "File $1 is not a gzipped file!"
  exit 3
fi  

zcat $1 | most

exit 0

# Uses the file viewer 'most'
# (similar to 'less')
