#!/bin/bash
# subshell.sh

echo

echo "We are outside the subshell."
echo "Subshell level OUTSIDE subshell = $BASH_SUBSHELL"
# Bash, version 3, adds the new         $BASH_SUBSHELL variable.
echo; echo

outer_variable=Outer
global_variable=
#  Define global variable for "storage" of
#+ value of subshell variable.

(
echo "We are inside the subshell."
echo "Subshell level INSIDE subshell = $BASH_SUBSHELL"
inner_variable=Inner

echo "From inside subshell, \"inner_variable\" = $inner_variable"
echo "From inside subshell, \"outer\" = $outer_variable"

global_variable="$inner_variable"   #  Will this allow "exporting"
                                    #+ a subshell variable?
)

echo; echo
echo "We are outside the subshell."
echo "Subshell level OUTSIDE subshell = $BASH_SUBSHELL"
echo

if [ -z "$inner_variable" ]
then
  echo "inner_variable undefined in main body of shell"
else
  echo "inner_variable defined in main body of shell"
fi

echo "From main body of shell, \"inner_variable\" = $inner_variable"
#  $inner_variable will show as blank (uninitialized)
#+ because variables defined in a subshell are "local variables".
#  Is there a remedy for this?
echo "global_variable = "$global_variable""  # Why doesn't this work?

echo

# =======================================================================

# Additionally ...

echo "-----------------"; echo

var=41                                                 # Global variable.

( let "var+=1"; echo "\$var INSIDE subshell = $var" )  # 42

echo "\$var OUTSIDE subshell = $var"                   # 41
#  Variable operations inside a subshell, even to a GLOBAL variable
#+ do not affect the value of the variable outside the subshell!


exit 0

#  Question:
#  --------
#  Once having exited a subshell,
#+ is there any way to reenter that very same subshell
#+ to modify or access the subshell variables?
