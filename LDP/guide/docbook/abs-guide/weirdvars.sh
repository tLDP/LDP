#!/bin/bash
# weirdvars.sh: Echoing weird variables.

var="'(]\\{}\$\""
echo $var        # '(]\{}$"
echo "$var"      # '(]\{}$"     Doesn't make a difference.

echo

IFS='\'
echo $var        # '(] {}$"     \ converted to space.
echo "$var"      # '(]\{}$"

# Examples above supplied by S.C.

exit 0
