#!/bin/bash

# "and list"

if [ ! -z $1 ] && echo "Argument #1 = $1" && [ ! -z $2 ] && echo "Argument #2 = $2"
then
  echo "At least 2 arguments to script."
  # All the chained commands return true.
else
  echo "Less than 2 arguments to script."
  # At least one of the chained commands returns false.
fi  
# Note that "if [ ! -z $1 ]" works, but its supposed equivalent,
# "if [ -n $1 ]" does not. This is a bug, not a feature.


# This accomplishes the same thing, coded using "pure" if/then statements.
if [ ! -z $1 ]
then
  echo "Argument #1 = $1"
fi
if [ ! -z $2 ]
then
  echo "Argument #2 = $2"
  echo "At least 2 arguments to script."
else
  echo "Less than 2 arguments to script."
fi
# It's longer and less elegant than using an "and list".


exit 0
