#!/bin/bash


area[11]=23
area[13]=37
area[51]=UFOs

# Note that array members need not be consecutive
# or contiguous.

# Some members of the array can be left uninitialized.
# Gaps in the array are o.k.

echo -n "area[11] = "
echo ${area[11]}
echo -n "area[13] = "
echo ${area[13]}
# Note that {curly brackets} needed
echo "Contents of area[51] are ${area[51]}."

# Contents of uninitialized array variable print blank.
echo -n "area[43] = "
echo ${area[43]}
echo "(area[43] unassigned)"

echo

# Sum of two array variables assigned to third
area[5]=`expr ${area[11]} + ${area[13]}`
echo "area[5] = area[11] + area[13]"
echo -n "area[5] = "
echo ${area[5]}

area[6]=`expr ${area[11]} + ${area[51]}`
echo "area[6] = area[11] + area[51]"
echo -n "area[6] = "
echo ${area[6]}
# This doesn't work because
# adding an integer to a string is not permitted.

exit 0
