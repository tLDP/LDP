#!/bin/bash
# Counting to 6 in 5 different ways.

n=1; echo -n "$n "

let "n = $n + 1"   # let "n = n + 1"   also works.
echo -n "$n "

: $((n = $n + 1))
# ":" necessary because otherwise Bash attempts
# to interpret "$((n = $n + 1))" as a command.
echo -n "$n "

n=$(($n + 1))
echo -n "$n "

: $[ n = $n + 1 ]
# ":" necessary because otherwise Bash attempts
# to interpret "$((n = $n + 1))" as a command.
# Works even if "n" was initialized as a string.
echo -n "$n "

n=$[ $n + 1 ]
# Works even if "n" was initialized as a string.
# Avoid this type of construct, since it is obsolete and nonportable.
echo -n "$n "; echo

# Thanks, Stephane Chazelas.

exit 0
