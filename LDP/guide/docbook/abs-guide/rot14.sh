#!/bin/bash
# A version of "rot13" using 'eval'.
# Compare to "rot13.sh" example.

setvar_rot_13()              # "rot13" scrambling
{
  local varname=$1 varvalue=$2
  eval $varname='$(echo "$varvalue" | tr a-z n-za-m)'
}


setvar_rot_13 var "foobar"   # Run "foobar" through rot13.
echo $var                    # sbbone

setvar_rot_13 var "$var"     # Run "sbbone" through rot13.
                             # Back to original variable.
echo $var                    # foobar

# This example by Stephane Chazelas.
# Modified by document author.

exit 0
