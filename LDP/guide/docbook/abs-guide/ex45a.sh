#!/bin/bash

echo
echo "String operations using \"expr $string :\" construct"
echo "-------------------------------------------"
echo

a=1234zipper43231
echo "The string being operated upon is \"`expr "$a" : '\(.*\)'`\"."
#       Escaped parentheses.
#       Regular expression parsing.

echo "Length of \"$a\" is `expr "$a" : '.*'`."   # Length of string

echo "Number of digits at the beginning of \"$a\" is `expr "$a" : '[0-9]*'`."

echo "The digits at the beginning of \"$a\" are `expr "$a" : '\([0-9]*\)'`."

echo

exit 0
