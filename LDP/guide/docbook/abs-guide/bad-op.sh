#!/bin/bash
# bad-op.sh: Trying to use a string comparison on integers.

echo
number=1

#  The following while-loop has two errors:
#+ one blatant, and the other subtle.

while [ "$number" &lt; 5 ]    # Wrong! Should be:  while [ "$number" -lt 5 ]
do
  echo -n "$number "
  let "number += 1"
done  
#  Attempt to run this bombs with the error message:
#+ bad-op.sh: line 10: 5: No such file or directory
#  Within single brackets, "&lt;" must be escaped,
#+ and even then, it's still wrong for comparing integers.

echo "---------------------"

while [ "$number" \&lt; 5 ]    #  1 2 3 4
do                          #
  echo -n "$number "        #  It *seems* to work, but . . .
  let "number += 1"         #+ it actually does an ASCII comparison,
done                        #+ rather than a numerical one.

echo; echo "---------------------"

# This can cause problems. For example:

lesser=5
greater=105

if [ "$greater" \&lt; "$lesser" ]
then
  echo "$greater is less than $lesser"
fi                          # 105 is less than 5
#  In fact, "105" actually is less than "5"
#+ in a string comparison (ASCII sort order).

echo

exit 0
