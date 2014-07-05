#!/bin/bash

ARGS=1        # Number of arguments expected.
E_BADARGS=85  # Exit value if incorrect number of args passed.

test $# -ne $ARGS &amp;&amp; \
#    ^^^^^^^^^^^^ condition #1
echo "Usage: `basename $0` $ARGS argument(s)" &amp;&amp; exit $E_BADARGS
#                                             ^^
#  If condition #1 tests true (wrong number of args passed to script),
#+ then the rest of the line executes, and script terminates.

# Line below executes only if the above test fails.
echo "Correct number of arguments passed to this script."

exit 0

# To check exit value, do a "echo $?" after script termination.
