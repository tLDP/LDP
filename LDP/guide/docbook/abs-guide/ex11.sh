#!/bin/bash

echo


if test -z "$1"
then
  echo "No command-line arguments."
else
  echo "First command-line argument is $1."
fi

# Both code blocks are functionally identical.

if [ -z "$1" ]
# if [ -z "$1"
# also works, but outputs an error message.
then
  echo "No command-line arguments."
else
  echo "First command-line argument is $1."
fi


echo

exit 0
