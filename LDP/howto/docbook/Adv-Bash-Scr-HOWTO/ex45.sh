#!/bin/bash

# Demonstrating some of the uses of 'expr'
# +++++++++++++++++++++++++++++++++++++++

echo

# Arithmetic Operators

echo Arithmetic Operators
echo
a=`expr 5 + 3`
echo 5 + 3 = $a

a=`expr $a + 1`
echo
echo a + 1 = $a
echo \(incrementing a variable\)

a=`expr 5 % 3`
# modulo
echo
echo 5 mod 3 = $a

echo
echo

# Logical Operators

echo Logical Operators
echo

a=3
echo a = $a
b=`expr $a \> 10`
echo 'b=`expr $a \> 10`, therefore...'
echo "If a > 10, b = 0 (false)"
echo b = $b

b=`expr $a \< 10`
echo "If a < 10, b = 1 (true)"
echo b = $b


echo
echo

# Comparison Operators

echo Comparison Operators
echo
a=zipper
echo a is $a
if [ `expr $a = snap` ]
# Force re-evaluation of variable 'a'
then
   echo "a is not zipper"
fi   

echo
echo

# String Operators

echo String Operators
echo

a=1234zipper43231
echo The string being operated upon is $a.
# index: position of substring
b=`expr index $a 23`
echo Numerical position of first 23 in $a is $b.
# substr: print substring, starting position & length specified
b=`expr substr $a 2 6`
echo Substring of $a, starting at position 2 and 6 chars long is $b.
# length: length of string
b=`expr length $a`
echo Length of $a is $b.
# 'match' operations similarly to 'grep'
b=`expr match $a [0-9]*`
echo Number of digits at the beginning of $a is $b.
b=`expr match $a '\([0-9]*\)'`
echo The digits at the beginning of $a are $b.

echo

exit 0
