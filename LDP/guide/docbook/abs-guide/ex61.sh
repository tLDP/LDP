#!/bin/bash

# Arabic number to Roman numeral conversion
# Range 0 - 200
# It's crude, but it works.

# Extending the range and otherwise improving the script
# is left as an exercise for the reader.

# Usage: roman number-to-convert

ARG_ERR=65
LIMIT=200

if [ -z "$1" ]
then
  echo "Usage: `basename $0` number-to-convert"
  exit $ARG_ERR
fi  

num=$1
if [ "$num" -gt $LIMIT ]
then
  echo "Out of range!"
  exit $OUT_OF_RANGE
fi  

to_roman ()
{
number=$1
factor=$2
rchar=$3
let "remainder = number - factor"
while [ "$remainder" -ge 0 ]
do
  echo -n $rchar
  let "number -= factor"
  let "remainder = number - factor"
done  

return $number
}

# Note: must declare function
#       before first call to it.

to_roman $num 100 C
num=$?
to_roman $num 90 LXXXX
num=$?
to_roman $num 50 L
num=$?
to_roman $num 40 XL
num=$?
to_roman $num 10 X
num=$?
to_roman $num 9 IX
num=$?
to_roman $num 5 V
num=$?
to_roman $num 4 IV
num=$?
to_roman $num 1 I

echo

exit 0
