#!/bin/bash
# multiplication.sh

multiply ()                   # Multiplies params passed.
{

  local product=1

  until [ -z "$1" ]           # Until uses up arguments passed...
  do
    let "product *= $1"
    shift
  done

  echo $product               #  Will not echo to stdout,
}                             #+ since this will be assigned to a variable.

val1=`multiply 15383 25211`
echo "val1 = $val1"           # 387820813

val2=`multiply 25 5 20`
echo "val2 = $val2"           # 2500

val3=`multiply 188 37 25 47`
echo "val3 = $val3"           # 8173300

exit 0
