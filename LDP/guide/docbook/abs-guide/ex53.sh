#!/bin/bash

for a in `seq 80`  # or   for a in $( seq 80 )
# Same as   for a in 1 2 3 4 5 ... 80   (saves much typing!).
# May also use 'jot' (if present on system).
do
  echo -n "$a "
done
# Example of using the output of a command to generate 
# the [list] in a "for" loop.

echo; echo


COUNT=80  # Yes, 'seq' may also take a replaceable parameter.

for a in `seq $COUNT`  # or   for a in $( seq $COUNT )
do
  echo -n "$a "
done

echo

exit 0
