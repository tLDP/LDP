#!/bin/bash

for a in `seq 80`
# Same as   for a in 1 2 3 4 5 ... 80   (saves much typing!).
# May also use 'jot' (if present on system).
do
  echo -n "$a "
done

echo

exit 0
