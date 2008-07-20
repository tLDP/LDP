#!/bin/bash

# Arabic number to Roman numeral conversion
# Range: 0 - 200
# It's crude, but it works.

# Extending the range and otherwise improving the script is left as an exercise.

# Usage: roman number-to-convert

LIMIT=200
E_ARG_ERR=65
E_OUT_OF_RANGE=66

if [ -z "$1" ]
then
  echo "Usage: `basename $0` number-to-convert"
  exit $E_ARG_ERR
fi  

num=$1
if [ "$num" -gt $LIMIT ]
then
  echo "Out of range!"
  exit $E_OUT_OF_RANGE
fi  

to_roman ()   # Must declare function before first call to it.
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
       # Exercises:
       # ---------
       # 1) Explain how this function works.
       #    Hint: division by successive subtraction.
       # 2) Extend to range of the function.
       #    Hint: use "echo" and command-substitution capture.
}
   

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
# Successive calls to conversion function!
# Is this really necessary??? Can it be simplified?

echo

exit
