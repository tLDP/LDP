#!/bin/bash
# max2.sh: Maximum of two LARGE integers.

#  This is the previous "max.sh" example,
#+ modified to permit comparing large integers.

EQUAL=0             # Return value if both params equal.
E_PARAM_ERR=-99999  # Not enough params passed to function.

max2 ()             # "Returns" larger of two numbers.
{
if [ -z "$2" ]
then
  echo $E_PARAM_ERR
  return
fi

if [ "$1" -eq "$2" ]
then
  echo $EQUAL
  return
else
  if [ "$1" -gt "$2" ]
  then
    retval=$1
  else
    retval=$2
  fi
fi

echo $retval        # Echoes, rather than returning value.

}


return_val=$(max2 33001 33997)
# Advanced parameter substitition.
# Assigns the stdout of function to the variable 'return_val' . . .


if [ "$return_val" -eq "$E_PARAM_ERR" ]
  then
  echo "Error in parameters passed to comparison function!"
elif [ "$return_val" -eq "$EQUAL" ]
  then
    echo "The two numbers are equal."
else
    echo "The larger of the two numbers is $return_val."
fi  
  
exit 0

#  Exercise:
#  --------
#  Find a more elegant way of testing
#+ the parameters passed to the function.
