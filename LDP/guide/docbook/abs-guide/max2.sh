#!/bin/bash
# max2.sh: Maximum of two LARGE integers.

# This is the previous "max.sh" example,
# modified to permit comparing large integers.

EQUAL=0             # Return value if both params equal.
MAXRETVAL=256       # Maximum positive return value from a function.
E_PARAM_ERR=-99999  # Parameter error.
E_NPARAM_ERR=99999  # "Normalized" parameter error.

max2 ()             # Returns larger of two numbers.
{
if [ -z "$2" ]
then
  return $E_PARAM_ERR
fi

if [ "$1" -eq "$2" ]
then
  return $EQUAL
else
  if [ "$1" -gt "$2" ]
  then
    retval=$1
  else
    retval=$2
  fi
fi

# -------------------------------------------------------------- #
# This is a workaround to enable returning a large integer
# from this function.
if [ "$retval" -gt "$MAXRETVAL" ]    # If out of range,
then                                 # then
  let "retval = (( 0 - $retval ))"   # adjust to a negative value.
  # (( 0 - $VALUE )) changes the sign of VALUE.
fi
# Large *negative* return values permitted, fortunately.
# -------------------------------------------------------------- #

return $retval
}

max2 33001 33997
return_val=$?

# -------------------------------------------------------------------------- #
if [ "$return_val" -lt 0 ]                  # If "adjusted" negative number,
then                                        # then
  let "return_val = (( 0 - $return_val ))"  # renormalize to positive.
fi                                          # "Absolute value" of $return_val.  
# -------------------------------------------------------------------------- #


if [ "$return_val" -eq "$E_NPARAM_ERR" ]
then                   # Parameter error "flag" gets sign changed, too.
  echo "Error: Too few parameters."
elif [ "$return_val" -eq "$EQUAL" ]
  then
    echo "The two numbers are equal."
else
    echo "The larger of the two numbers is $return_val."
fi  
  
exit 0
