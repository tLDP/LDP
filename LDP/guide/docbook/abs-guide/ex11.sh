#!/bin/bash

echo

if test -z "$1"
then
  echo "No command-line arguments."
else
  echo "First command-line argument is $1."
fi

# Both code blocks are functionally identical.

if [ -z "$1" ]   # if [ -z "$1"   should work, but...
# Bash responds to a missing close bracket with an error message.
then
  echo "No command-line arguments."
else
  echo "First command-line argument is $1."
fi

echo

exit 0
