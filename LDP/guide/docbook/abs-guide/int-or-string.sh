#!/bin/bash
# int-or-string.sh
# Integer or string?

a=2334                   # Integer.
let "a += 1"
echo "a = $a "           # Integer, still.
echo

b=${a/23/BB}             # Transform into a string.
echo "b = $b"            # BB35
declare -i b             # Declaring it an integer doesn't help.
echo "b = $b"            # BB35, still.

let "b += 1"             # BB35 + 1 =
echo "b = $b"            # 1
echo

c=BB34
echo "c = $c"            # BB34
d=${c/BB/23}             # Transform into an integer.
echo "d = $d"            # 2334
let "d += 1"             # 2334 + 1 =
echo "d = $d"            # 2335

# Variables in Bash are essentially untyped.

exit 0
