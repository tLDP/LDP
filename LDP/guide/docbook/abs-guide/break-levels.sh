#!/bin/bash
# Breaking out of loops.

# "break N" breaks out of N level loops.

for outerloop in 1 2 3 4 5
do
  echo -n "Group $outerloop:   "

  for innerloop in 1 2 3 4 5
  do
    echo -n "$innerloop "

    if [ "$innerloop" -eq 3 ]
    then
      break
      # Replace the line above with     break 2
      # to see what happens ("breaks" out of both inner and outer loops.)
    fi

  done

  echo
done  

echo

exit 0
