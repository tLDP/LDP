#!/bin/bash

y=`eval ls -l`  #  Similar to y=`ls -l`
echo $y         #+ but linefeeds removed because "echoed" variable is unquoted.
echo
echo "$y"       #  Linefeeds preserved when variable is quoted.

echo; echo

y=`eval df`     #  Similar to y=`df`
echo $y         #+ but linefeeds removed.

#  When LF's not preserved, it may make it easier to parse output,
#+ using utilities such as "awk".

echo
echo "==========================================================="
echo

# Now, showing how to "expand" a variable using "eval" . . .

for i in 1 2 3 4 5; do
  eval value=$i
  #  value=$i has same effect. The "eval" is not necessary here.
  #  A variable lacking a meta-meaning evaluates to itself --
  #+ it can't expand to anything other than its literal self.
  echo $value
done

echo
echo "---"
echo

for i in ls df; do
  value=eval $i
  #  value=$i has an entirely different effect here.
  #  The "eval" evaluates the commands "ls" and "df" . . .
  #  The terms "ls" and "df" have a meta-meaning,
  #+ since they are interpreted as commands,
  #+ rather than just character strings.
  echo $value
done


exit 0
