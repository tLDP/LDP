#!/bin/bash

until [ "$var1" = end ] # Tests condition here, at top of loop.
do
  echo "Input variable #1 "
  echo "(end to exit)"
  read var1
  echo "variable #1 = $var1"
done  

exit 0
