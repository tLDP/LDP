#!/bin/bash
# Using "case" structure to filter a string.

SUCCESS=0
FAILURE=-1

isalpha ()  # Tests whether *first character* of input string is alphabetic.
{
if [ -z "$1" ]                # No argument passed?
then
  return $FAILURE
fi

case "$1" in
[a-zA-Z]*) return $SUCCESS;;  # Begins with a letter?
*        ) return $FAILURE;;
esac
}             # Compare this with "isalpha ()" function in C.


isalpha2 ()   # Tests whether *entire string* is alphabetic.
{
  [ $# -eq 1 ] || return $FAILURE

  case $1 in
  *[!a-zA-Z]*|"") return $FAILURE;;
               *) return $SUCCESS;;
  esac
}



check_var ()  # Front-end to isalpha().
{
if isalpha "$@"
then
  echo "$* = alpha"
else
  echo "$* = non-alpha"  # Also "non-alpha" if no argument passed.
fi
}

a=23skidoo
b=H3llo
c=-What?
d=`echo $b`   # Command substitution.

check_var $a
check_var $b
check_var $c
check_var $d
check_var     # No argument passed, so what happens?


# Script improved by S.C.

exit 0
