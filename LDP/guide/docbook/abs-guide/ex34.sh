#!/bin/bash

# script "set-test"

# Invoke this script with three command line parameters,
# for example, "./set-test one two three".

echo
echo "Positional parameters before  set \`uname -a\` :"
echo "Command-line argument #1 = $1"
echo "Command-line argument #2 = $2"
echo "Command-line argument #3 = $3"


set `uname -a` # Sets the positional parameters to the output
               # of the command `uname -a`

echo $_        # unknown
# Flags set in script.

echo "Positional parameters after  set \`uname -a\` :"
# $1, $2, $3, etc. reinitialized to result of `uname -a`
echo "Field #1 of 'uname -a' = $1"
echo "Field #2 of 'uname -a' = $2"
echo "Field #3 of 'uname -a' = $3"
echo ---
echo $_        # ---
echo

exit 0
