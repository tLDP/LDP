#!/bin/bash

declare -f
# Lists the function below.

func1 ()
{
echo This is a function.
}

declare -r var1=13.36
echo "var1 declared as $var1"
# Attempt to change readonly variable.
var1=13.37
# Generates error message.
echo "var1 is still $var1"

echo

declare -i var2
var2=2367
echo "var2 declared as $var2"
var2=var2+1
# Integer declaration eliminates the need for 'let'.
echo "var2 incremented by 1 is $var2."
# Attempt to change variable declared as integer
echo "Attempting to change var2 to floating point value, 2367.1."
var2=2367.1
# results in error message, with no change to variable.
echo "var2 is still $var2"

exit 0
