#!/bin/bash
# recurse.sh

#  Can a script recursively call itself?
#  Yes, but is this of any practical use?
#  (See the following.)

RANGE=10
MAXVAL=9

i=$RANDOM
let "i %= $RANGE"  # Generate a random number between 0 and $RANGE - 1.

if [ "$i" -lt "$MAXVAL" ]
then
  echo "i = $i"
  ./$0             #  Script recursively spawns a new instance of itself.
fi                 #  Each child script does the same, until
                   #+ a generated $i equals $MAXVAL.

#  Using a "while" loop instead of an "if/then" test causes problems.
#  Explain why.

exit 0

# Note:
# ----
# This script must have execute permission for it to work properly.
# This is the case even if it is invoked by an "sh" command.
# Explain why.
