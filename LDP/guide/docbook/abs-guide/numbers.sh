#!/bin/bash
# numbers.sh: Representation of numbers.

# Decimal
let "d = 32"
echo "d = $d"
# Nothing out of the ordinary here.


# Octal: numbers preceded by '0' (zero)
let "o = 071"
echo "o = $o"
# Expresses result in decimal.

# Hexadecimal: numbers preceded by '0x' or '0X'
let "h = 0x7a"
echo "h = $h"
# Expresses result in decimal.

# Other bases: BASE#NUMBER
# BASE between 2 and 36.
let "b = 32#77"
echo "b = $b"
# This notation only works for a limited range (2 - 36)
            # ... 10 digits + 26 alpha characters = 36.
let "c = 2#47"  # Error: out of range.
echo "c = $c"

echo

echo $((36#zz)) $((2#10101010)) $((16#AF16))

exit 0
# Thanks, S.C., for clarification.
