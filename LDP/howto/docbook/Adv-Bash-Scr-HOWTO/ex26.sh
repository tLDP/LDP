#!/bin/bash

while [ "$var1" != end ]
do
  echo "Input variable #1 "
  echo "(end to exit)"
  read var1
  # It's not 'read $var1'
  # because value of var1 is set.
  echo "variable #1 = $var1"
  # Need quotes because of #
done  

# Note: Echoes 'end' because
# termination condition
# tested for at top of loop.

exit 0
