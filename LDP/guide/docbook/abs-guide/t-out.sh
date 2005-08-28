#!/bin/bash
# t-out.sh
# Inspired by a suggestion from "syngin seven" (thanks).


TIMELIMIT=4         # 4 seconds

read -t $TIMELIMIT variable <&1
#                           ^^^
#  In this instance, "<&1" is needed for Bash 1.x and 2.x,
#  but unnecessary for Bash 3.x.

echo

if [ -z "$variable" ]  # Is null?
then
  echo "Timed out, variable still unset."
else  
  echo "variable = $variable"
fi  

exit 0
