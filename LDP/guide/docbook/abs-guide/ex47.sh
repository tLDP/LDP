#!/bin/bash

# printf demo

PI=3.14159265358979
DecimalConstant=31373
Message1="Greetings,"
Message2="Earthling."

echo

printf "Pi to 2 decimal places = %1.2f" $PI
echo
printf "Pi to 9 decimal places = %1.9f" $PI
# Note correct round off.

printf "\n"
# Prints a line feed, equivalent to 'echo'.

printf "Constant = \t%d\n" $DecimalConstant
# Insert tab (\t)

printf "%s %s \n" $Message1 $Message2

echo

exit 0
