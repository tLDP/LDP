#!/bin/bash
# primes.sh: generate prime numbers, without using arrays.

# This does *not* use the classic "Sieve of Erastosthenes" algorithm,
# but instead uses the more intuitive method of testing each candidate number
# for factors (divisors) up to half its value, using the "%" modulo operator.
#
# Script contributed by Stephane Chazelas,


LIMIT=1000  # Primes 2 - 1000

Primes()
{
 (( n = $1 + 1 ))             # Bump to next integer.
 shift
 
 if (( n == LIMIT ))
 then echo $*
 return
 fi

 for i; do
   (( i * i > n )) && break   # Need check divisors only halfway to top.
   (( n % i )) && continue    # Sift out non-primes using modulo operator.
   Primes $n $@               # Recursion.
   return
   done

   Primes $n $@ $n            # Recursion.
}

Primes 1

# This may also be rewritten without recursion for faster execution.

exit 0

# Compare the speed of this algorithm for generating primes
# with the Sieve of Erastosthenes (ex68.sh).
