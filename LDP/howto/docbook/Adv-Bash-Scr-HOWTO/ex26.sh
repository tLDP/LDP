#!/bin/bash

echo

while [ "$var1" != end ]
do
  echo "Input variable #1 (end to exit) "
  read var1
  # It's not 'read $var1' because value of var1 is being set.
  echo "variable #1 = $var1"
  # Need quotes because of #
  echo
done  

# Note: Echoes 'end' because termination condition tested for at top of loop.

exit 0
