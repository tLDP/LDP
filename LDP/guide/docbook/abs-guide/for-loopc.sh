#!/bin/bash
# Two ways to count up to 10.

echo

# Standard syntax.
for a in 1 2 3 4 5 6 7 8 9 10
do
  echo -n "$a "
done  

echo; echo

# +==========================================+

# Now, let's do the same, using C-like syntax.

LIMIT=10

for ((a=1; a <= LIMIT ; a++))  # Double parentheses, and "LIMIT" with no "$".
do
  echo -n "$a "
done                           # A construct borrowed from 'ksh93'.

echo; echo

# +=========================================================================+

# Let's use the C "comma operator" to increment two variables simultaneously.

for ((a=1, b=1; a <= LIMIT ; a++, b++))  # The comma chains together operations.
do
  echo -n "$a-$b "
done

echo; echo

exit 0
