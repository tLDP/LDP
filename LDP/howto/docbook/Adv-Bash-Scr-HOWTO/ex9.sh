#!/bin/bash

# Variables: assignment and substitution

a=37.5
hello=$a
# No space permitted on either side of = sign when initializing variables.

echo hello
# Not a reference.

echo $hello
echo ${hello} #Identical to above.

echo "$hello"
echo "${hello}"

echo '$hello'
# Variable referencing disabled by single quotes,
# because $ interpreted literally.

# Notice the effect of different types of quoting.

# ------------------------------------------------

echo; echo

numbers="one two three"
other_numbers="1 2 3"
# If whitespace within variables, then quotes necessary.
echo "numbers = $numbers"
echo "other_numbers = $other_numbers"
echo

echo "uninitialized variable = $uninitialized_variable"
# Uninitialized variable has null value (no value at all).

echo

exit 0
