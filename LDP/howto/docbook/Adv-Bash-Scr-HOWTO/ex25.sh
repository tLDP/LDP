#!/bin/bash

var0=0

while [ "$var0" -lt 10 ]
do
  echo -n "$var0 "
  # -n suppresses newline.
  var0=`expr $var0 + 1`
  # var0=$(($var0+1)) also works.
done

echo

exit 0
