#!/bin/bash
# "and list"

if [ ! -z "$1" ] && echo "Argument #1 = $1" && [ ! -z "$2" ] \
&& echo "Argument #2 = $2"
then
  echo "At least 2 arguments passed to script."
  # All the chained commands return true.
else
  echo "Less than 2 arguments passed to script."
  # At least one of the chained commands returns false.
fi  
# Note that "if [ ! -z $1 ]" works, but its supposed equivalent,
#   if [ -n $1 ] does not.
#     However, quoting fixes this.
#  if [ -n "$1" ] works.
#     Careful!
# It is always best to QUOTE tested variables.


# This accomplishes the same thing, using "pure" if/then statements.
if [ ! -z "$1" ]
then
  echo "Argument #1 = $1"
fi
if [ ! -z "$2" ]
then
  echo "Argument #2 = $2"
  echo "At least 2 arguments passed to script."
else
  echo "Less than 2 arguments passed to script."
fi
# It's longer and less elegant than using an "and list".


exit 0
