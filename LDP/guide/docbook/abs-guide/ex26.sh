#!/bin/bash

echo

while [ "$var1" != "end" ]     # while test "$var1" != "end"
do                             # also works.
  echo "Input variable #1 (end to exit) "
  read var1                    # Not 'read $var1' (why?).
  echo "variable #1 = $var1"   # Need quotes because of "#".
  # If input is 'end', echoes it here.
  # Does not test for termination condition until top of loop.
  echo
done  

exit 0
