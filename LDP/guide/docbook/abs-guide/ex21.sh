#!/bin/bash

# $RANDOM returns a different random integer at each invocation.
# Nominal range: 0 - 32767 (signed 16-bit integer).

MAXCOUNT=10
count=1

echo
echo "$MAXCOUNT random numbers:"
echo "-----------------"
while [ "$count" -le $MAXCOUNT ]      # Generate 10 ($MAXCOUNT) random integers.
do
  number=$RANDOM
  echo $number
  let "count += 1"  # Increment count.
done
echo "-----------------"

# If you need a random int within a certain range, use the 'modulo' operator.
# This returns the remainder of a division operation.

RANGE=500

echo

number=$RANDOM
let "number %= $RANGE"
echo "Random number less than $RANGE  ---  $number"

echo

# If you need a random int greater than a lower bound,
# then set up a test to discard all numbers below that.

FLOOR=200

number=0   #initialize
while [ "$number" -le $FLOOR ]
do
  number=$RANDOM
done
echo "Random number greater than $FLOOR ---  $number"
echo


# May combine above two techniques to retrieve random number between two limits.
number=0   #initialize
while [ "$number" -le $FLOOR ]
do
  number=$RANDOM
  let "number %= $RANGE"  # Scales $number down within $RANGE.
done
echo "Random number between $FLOOR and $RANGE ---  $number"
echo


# Generate binary choice, that is, "true" or "false" value.
BINARY=2
number=$RANDOM
T=1

let "number %= $BINARY"
# let "number >>= 14"    gives a better random distribution
# (right shifts out everything except last binary digit).
if [ "$number" -eq $T ]
then
  echo "TRUE"
else
  echo "FALSE"
fi  

echo


# May generate toss of the dice.
SPOTS=7   # Modulo 7 gives range 0 - 6.
ZERO=0
die1=0
die2=0

# Tosses each die separately, and so gives correct odds.

  while [ "$die1" -eq $ZERO ]     # Can't have a zero come up.
  do
    let "die1 = $RANDOM % $SPOTS" # Roll first one.
  done  

  while [ "$die2" -eq $ZERO ]
  do
    let "die2 = $RANDOM % $SPOTS" # Roll second one.
  done  

let "throw = $die1 + $die2"
echo "Throw of the dice = $throw"
echo


exit 0
