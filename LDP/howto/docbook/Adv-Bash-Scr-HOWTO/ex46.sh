#!/bin/bash

echo

let a=11
# Same as 'a=11'
let a=a+5
# Equivalent to let "a = a + 5"
# (double quotes makes it more readable)
echo "a = $a"
let "a <<= 3"
# Equivalent of let "a = a << 3"
echo "a left-shifted 3 places = $a"

let "a /= 4"
# Equivalent to let "a = a / 4"
echo $a
let "a -= 5"
# Equivalent to let "a = a - 5"
echo $a
let "a = a * 10"
echo $a
let "a %= 8"
echo $a

exit 0
