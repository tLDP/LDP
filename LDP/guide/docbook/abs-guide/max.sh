#!/bin/bash

PARAM_ERR=-198  # If less than 2 params passed to function.
EQUAL=-199      # Return value if both params equal.

max2 ()  # Returns larger of two numbers.
{
if [ -z "$2" ]
then
  return $PARAM_ERR
fi

if [ "$1" -eq "$2" ]
then
  return $EQUAL
else
  if [ "$1" -gt "$2" ]
  then
    return $1
  else
    return $2
  fi
fi
}

max2 33 34
return_val=$?

if [ "$return_val" -eq $PARAM_ERR ]
then
  echo "Need to pass two parameters to the function."
elif [ "$return_val" -eq $EQUAL ]
  then
    echo "The two numbers are equal."
else
    echo "The larger of the two numbers is $return_val."
fi  

  
exit 0

# Exercise for the reader (easy):
# Convert this to an interactive script,
# that is, have the script ask for input (two numbers).
