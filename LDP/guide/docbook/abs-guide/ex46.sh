#!/bin/bash

echo

let a=11          # Same as 'a=11'
let a=a+5         # Equivalent to  let "a = a + 5"
                  # (double quotes and spaces make it more readable)
echo "11 + 5 = $a"

let "a <<= 3"     # Equivalent to  let "a = a << 3"
echo "\"\$a\" (=16) left-shifted 3 places = $a"

let "a /= 4"      # Equivalent to  let "a = a / 4"
echo "128 / 4 = $a"

let "a -= 5"      # Equivalent to  let "a = a - 5"
echo "32 - 5 = $a"

let "a = a * 10"  # Equivalent to  let "a = a * 10"
echo "27 * 10 = $a"

let "a %= 8"      # Equivalent to  let "a = a % 8"
echo "270 modulo 8 = $a  (270 / 8 = 33, remainder $a)"

echo

exit 0
