#!/bin/bash

if [ 0 ]
#zero
then
  echo "0 is true."
else
  echo "0 is false."
fi

if [ ]
#NULL (empty condition)
then
  echo "NULL is true."
else
  echo "NULL is false."
fi

if [ xyz ]
#string
then
  echo "Random string is true."
else
  echo "Random string is false."
fi

if [ $xyz ]
#string
then
  echo "Undeclared variable is true."
else
  echo "Undeclared variable is false."
fi

exit 0
