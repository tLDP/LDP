#!/bin/bash

ARGS=2  # Two args to script expected.
E_BADARGS=65

if [ $# -ne "$ARGS" ]
then
  echo "Usage: `basename $0` file1 file2"
  exit $E_BADARGS
fi


cmp $1 $2 > /dev/null  # /dev/null buries the output of the "cmp" command.
# Also works with 'diff', i.e.,   diff $1 $2 > /dev/null

if [ $? -eq 0 ]        # Test exit status of "cmp" command.
then
  echo "File \"$1\" is identical to file \"$2\"."
else  
  echo "File \"$1\" differs from file \"$2\"."
fi

exit 0
