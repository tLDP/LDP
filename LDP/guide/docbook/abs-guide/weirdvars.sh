#!/bin/bash
# Echoing weird variables.

var="'(]\\{}\$\""
echo $var        # '(]\{}$"
echo "$var"      # '(]\{}$"     Doesn't make a difference.

IFS='\'
echo $var        # '(]\{}$"
echo "$var"      # '(] {}$"     \ converted to space.

# Examples above supplied by Stephane Chazelas.
exit 0
