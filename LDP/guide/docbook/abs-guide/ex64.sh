#!/bin/bash
# and list

if [ ! -z "$1" ] &amp;&amp; echo "Argument #1 = $1" &amp;&amp; [ ! -z "$2" ] &amp;&amp; \
#                ^^                         ^^               ^^
echo "Argument #2 = $2"
then
  echo "At least 2 arguments passed to script."
  # All the chained commands return true.
else
  echo "Fewer than 2 arguments passed to script."
  # At least one of the chained commands returns false.
fi  
# Note that "if [ ! -z $1 ]" works, but its alleged equivalent,
#   "if [ -n $1 ]" does not.
#     However, quoting fixes this.
#  if "[ -n "$1" ]" works.
#           ^  ^    Careful!
# It is always best to QUOTE the variables being tested.


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
  echo "Fewer than 2 arguments passed to script."
fi
# It's longer and more ponderous than using an "and list".


exit $?
