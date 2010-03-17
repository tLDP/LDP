#!/bin/bash
# Counting to 11 in 10 different ways.

n=1; echo -n "$n "

let "n = $n + 1"   # let "n = n + 1"  also works.
echo -n "$n "


: $((n = $n + 1))
#  ":" necessary because otherwise Bash attempts
#+ to interpret "$((n = $n + 1))" as a command.
echo -n "$n "

(( n = n + 1 ))
#  A simpler alternative to the method above.
#  Thanks, David Lombard, for pointing this out.
echo -n "$n "

n=$(($n + 1))
echo -n "$n "

: $[ n = $n + 1 ]
#  ":" necessary because otherwise Bash attempts
#+ to interpret "$[ n = $n + 1 ]" as a command.
#  Works even if "n" was initialized as a string.
echo -n "$n "

n=$[ $n + 1 ]
#  Works even if "n" was initialized as a string.
#* Avoid this type of construct, since it is obsolete and nonportable.
#  Thanks, Stephane Chazelas.
echo -n "$n "

# Now for C-style increment operators.
# Thanks, Frank Wang, for pointing this out.

let "n++"          # let "++n"  also works.
echo -n "$n "

(( n++ ))          # (( ++n ))  also works.
echo -n "$n "

: $(( n++ ))       # : $(( ++n )) also works.
echo -n "$n "

: $[ n++ ]         # : $[ ++n ] also works
echo -n "$n "

echo

exit 0
