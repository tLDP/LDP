#!/bin/bash

#               factorial
#               ---------


# Does bash permit recursion?
# Well, yes, but...
# You gotta have rocks in your head to try it.


MAX_ARG=5
WRONG_ARGS=1
RANGE_ERR=2


if [ -z $1 ]
then
  echo "Usage: `basename $0` number"
  exit $WRONG_ARGS
fi

if [ $1 -gt $MAX_ARG ]
then
  echo "Out of range (5 is maximum)."
  # Let's get real now...
  # If you want greater range than this, rewrite it in a real programming language.
  exit $RANGE_ERR
fi  

fact ()
{
  local number=$1
  # Variable "number" must be declared as local otherwise this doesn't work.
  if [ $number -eq 0 ]
  then
    factorial=1
  else
    let "decrnum = number - 1"
    fact $decrnum  # Recursive function call.
    let "factorial = $number * $?"
  fi

  return $factorial
}

fact $1
echo "Factorial of $1 is $?."

exit 0
