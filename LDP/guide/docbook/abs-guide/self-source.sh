#!/bin/bash
# self-source.sh: a script sourcing itself "recursively."
# From "Stupid Script Tricks," Volume II.

MAXPASSCNT=100    # Maximum number of execution passes.

echo -n  "$pass_count  "
#  At first execution pass, this just echoes two blank spaces,
#+ since $pass_count still uninitialized.

let "pass_count += 1"
#  Assumes the uninitialized variable $pass_count
#+ can be incremented the first time around.
#  This works with Bash and pdksh, but
#+ it relies on non-portable (and possibly dangerous) behavior.
#  Better would be to set $pass_count to 0 if non-initialized.

while [ "$pass_count" -le $MAXPASSCNT ]
do
  . $0   # Script "sources" itself, rather than calling itself.
         # ./$0 (which would be true recursion) doesn't work here.
done  

#  What occurs here is not actually recursion,
#+ since the script effectively "expands" itself
#+ (generates a new section of code)
#+ with each pass throught the 'while' loop',
#  with each 'source' in line 20.
#
#  Of course, the script interprets each newly 'sourced' "#!" line
#+ as a comment, and not as the start of a new script.

echo

exit 0   # The net effect is counting from 1 to 100.
         # Very impressive.

# Exercise:
# --------
# Write a script that uses this trick to do something useful.
