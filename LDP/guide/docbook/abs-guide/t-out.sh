#!/bin/bash
# t-out.sh
# Inspired by a suggestion from "syngin seven" (thanks).


TIMELIMIT=4         # 4 seconds

read -t $TIMELIMIT variable <&1

echo

if [ -z "$variable" ]
then
  echo "Timed out, variable still unset."
else  
  echo "variable = $variable"
fi  

exit 0

# Exercise for the reader:
# -----------------------
# Why is the redirection (<&1) necessary in line 8?
# What happens if it is omitted?
