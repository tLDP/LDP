#!/bin/bash

ENDLESS_LOOP=1
INTERVAL=1

echo
echo "Hit Control-C to exit this script."
echo

while [ $ENDLESS_LOOP ]
do
  if [ "$SECONDS" -eq 1 ]
  then
    units=second
  else  
    units=seconds
  fi

  echo "This script has been running $SECONDS $units."
  sleep $INTERVAL
done


exit 0
