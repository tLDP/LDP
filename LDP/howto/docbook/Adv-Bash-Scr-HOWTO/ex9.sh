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

# --------------------------------------------------------------

# It is permissible to set multiple variables on the same line,
# separated by white space. Careful, this may reduce legibility.

var1=variable1  var2=variable2  var3=variable3
echo
echo "var1=$var1   var2=$var2  var3=$var3"

# --------------------------------------------------------------

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
