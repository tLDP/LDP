#!/bin/bash

# Variables: assignment and substitution

a=37.5
hello=$a

#-------------------------------------------------------------------------
# No space permitted on either side of = sign when initializing variables.

# If "VARIABLE =value",
# script tries to run "VARIABLE" command with one argument, "=value".

# If "VARIABLE= value",
# script tries to run "value" command with
# the environmental variable "VARIABLE" set to "".
#-------------------------------------------------------------------------


echo hello
# Not a reference.

echo $hello
echo ${hello} #Identical to above.

echo "$hello"
echo "${hello}"

# hello="A B  C   D"
# Now,   echo $hello   and   echo "$hello"   give different results.
# Quoting variable perserves whitespace.

echo '$hello'
# Variable referencing disabled by single quotes,
# because $ interpreted literally.

# Notice the effect of different types of quoting.


# Now *unsetting* $hello.
hello=
echo "\$hello (unset) = $hello"
# Unsetting a variable means setting it to a null value.

# --------------------------------------------------------------

# It is permissible to set multiple variables on the same line,
# separated by white space.
# Careful, this may reduce legibility, and may not be portable.

var1=variable1  var2=variable2  var3=variable3
echo
echo "var1=$var1   var2=$var2  var3=$var3"

# This may cause problems with older versions of "sh".

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
