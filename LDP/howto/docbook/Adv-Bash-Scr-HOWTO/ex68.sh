#!/bin/bash

# sieve.sh
# Sieve of Erastosthenes
# Ancient algorithm for finding prime numbers.

# This runs a couple of orders of magnitude
# slower than equivalent C program.

LOWER_LIMIT=1
# Starting with 1.
UPPER_LIMIT=1000
# Up to 1000.
# (You may set this higher...
#  if you have time on your hands.)

PRIME=1
NON_PRIME=0

let SPLIT=UPPER_LIMIT/2
# Optimization:
# Need to test numbers only
# halfway to upper limit.


declare -a Primes
# Primes[] is an array.


initialize ()
{
# Initialize the array.

i=$LOWER_LIMIT
until [ $i -gt $UPPER_LIMIT ]
do
  Primes[i]=$PRIME
  let "i += 1"
done
# Assume all array members guilty (prime)
# until proven innocent.
}

print_primes ()
{
# Print out the members of the Primes[] array
# tagged as prime.

i=$LOWER_LIMIT

until [ $i -gt $UPPER_LIMIT ]
do

  if [ ${Primes[i]} -eq $PRIME ]
  then
    printf "%8d" $i
    # 8 spaces per number
    # gives nice, even columns.
  fi
  
  let "i += 1"
  
done

}

sift ()
{
# Sift out the non-primes.

let i=$LOWER_LIMIT+1
# We know 1 is prime, so
# let's start with 2.

until [ $i -gt $UPPER_LIMIT ]
do

if [ ${Primes[i]} -eq $PRIME ]
# Don't bother sieving numbers
# already sieved (tagged as non-prime).
then

  t=$i

  while [ $t -le $UPPER_LIMIT ]
  do
    let "t += $i "
    Primes[t]=$NON_PRIME
    # Tag as non-prime
    # all multiples.
  done

fi  

  let "i += 1"
done  


}


# Invoke the functions sequentially.
initialize
sift
print_primes
echo
# This is what they call structured programming.

exit 0
