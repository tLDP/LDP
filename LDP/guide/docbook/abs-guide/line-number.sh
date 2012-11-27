#!/bin/bash
# line-number.sh

# This script echoes itself twice to stdout with its lines numbered.

echo "     line number = $LINENO" # 'nl' sees this as line 4
#                                   (nl does not number blank lines).
#                                   'cat -n' sees it correctly as line #6.

nl `basename $0`

echo; echo  # Now, let's try it with 'cat -n'

cat -n `basename $0`
# The difference is that 'cat -n' numbers the blank lines.
# Note that 'nl -ba' will also do so.

exit 0
# -----------------------------------------------------------------
