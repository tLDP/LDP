#!/bin/bash

# Variables: assignment and substitution

a=375
hello=$a

#-------------------------------------------------------------------------
# No space permitted on either side of = sign when initializing variables.

#  If "VARIABLE =value",
#+ script tries to run "VARIABLE" command with one argument, "=value".

#  If "VARIABLE= value",
#+ script tries to run "value" command with
#+ the environmental variable "VARIABLE" set to "".
#-------------------------------------------------------------------------


echo hello    # Not a variable reference, just the string "hello".

echo $hello
echo ${hello} # Identical to above.

echo "$hello"
echo "${hello}"

echo

hello="A B  C   D"
echo $hello   # A B C D
echo "$hello" # A B  C   D
# As you see, echo $hello   and   echo "$hello"   give different results.
# Quoting a variable preserves whitespace.

echo

echo '$hello'  # $hello
#  Variable referencing disabled by single quotes,
#+ which causes the "$" to be interpreted literally.

# Notice the effect of different types of quoting.


hello=    # Setting it to a null value.
echo "\$hello (null value) = $hello"
#  Note that setting a variable to a null value is not the same as
#+ unsetting it, although the end result is the same (see below).

# --------------------------------------------------------------

#  It is permissible to set multiple variables on the same line,
#+ if separated by white space.
#  Caution, this may reduce legibility, and may not be portable.

var1=variable1  var2=variable2  var3=variable3
echo
echo "var1=$var1   var2=$var2  var3=$var3"

# May cause problems with older versions of "sh".

# --------------------------------------------------------------

echo; echo

numbers="one two three"
other_numbers="1 2 3"
# If whitespace within a variable, then quotes necessary.
echo "numbers = $numbers"
echo "other_numbers = $other_numbers"   # other_numbers = 1 2 3
echo

echo "uninitialized_variable = $uninitialized_variable"
# Uninitialized variable has null value (no value at all).
uninitialized_variable=   #  Declaring, but not initializing it
                          #+ (same as setting it to a null value, as above).
echo "uninitialized_variable = $uninitialized_variable"
                          # It still has a null value.

uninitialized_variable=23       # Set it.
unset uninitialized_variable    # Unset it.
echo "uninitialized_variable = $uninitialized_variable"
                                # It still has a null value.

echo

exit 0
