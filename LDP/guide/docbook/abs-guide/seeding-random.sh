#!/bin/bash
# seeding-random.sh: Seeding the RANDOM variable.

MAXCOUNT=25       # How many numbers to generate.

random_numbers ()
{
count=0
while [ "$count" -lt "$MAXCOUNT" ]
do
  number=$RANDOM
  echo -n "$number "
  let "count += 1"
done  
}

echo; echo

RANDOM=1          # Setting RANDOM seeds the random number generator.
random_numbers

echo; echo

RANDOM=1          # Same seed for RANDOM...
random_numbers    # ...reproduces the exact same number series.
                  #
                  # When is it useful to duplicate a "random" number series?

echo; echo

RANDOM=2          # Trying again, but with a different seed...
random_numbers    # gives a different number series.

echo; echo

# RANDOM=$$  seeds RANDOM from process id of script.
# It is also possible to seed RANDOM from 'time' or 'date' commands.

# Getting fancy...
SEED=$(head -1 /dev/urandom | od -N 1 | awk '{ print $2 }')
#  Pseudo-random output fetched
#+ from /dev/urandom (system pseudo-random device-file),
#+ then converted to line of printable (octal) numbers by "od",
#+ finally "awk" retrieves just one number for SEED.
RANDOM=$SEED
random_numbers

echo; echo

exit 0
