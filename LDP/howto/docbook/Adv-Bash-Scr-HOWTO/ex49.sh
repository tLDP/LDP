#!/bin/bash

# Changes a file to all uppercase.

if [ -z $1 ]
# Standard check whether command line arg is present.
then
  echo "Usage: `basename $0` filename"
  exit 1
fi  

tr [a-z] [A-Z] <$1

exit 0
