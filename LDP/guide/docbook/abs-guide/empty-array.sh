#!/bin/bash
# empty-array.sh

# An empty array is not the same as an array with empty elements.

array0=( first second third )
array1=( '' )   # "array1" has one empty element.
array2=( )      # No elements... "array2" is empty.

echo

echo "Elements in array0:  ${array0[@]}"
echo "Elements in array1:  ${array1[@]}"
echo "Elements in array2:  ${array2[@]}"
echo
echo "Length of first element in array0 = ${#array0}"
echo "Length of first element in array1 = ${#array1}"
echo "Length of first element in array2 = ${#array2}"
echo
echo "Number of elements in array0 = ${#array0[*]}"  # 3
echo "Number of elements in array1 = ${#array1[*]}"  # 1  (surprise!)
echo "Number of elements in array2 = ${#array2[*]}"  # 0

echo

# Thanks, S.C.

exit 0
