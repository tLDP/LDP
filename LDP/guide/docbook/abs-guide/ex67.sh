#!/bin/bash

declare -a colors
# Permits declaring an array without specifying size.

echo "Enter your favorite colors (separated from each other by a space)."

read -a colors
# Special option to 'read' command,
# allowing it to assign elements in an array.

echo

  element_count=${#colors[@]} # Special syntax to extract number of elements in array.
# element_count=${#colors[*]} works also.
#
# The "@" variable allows word splitting within quotes
# (extracts variables separated by whitespace).
index=0

# List all the elements in the array.
while [ "$index" -lt "$element_count" ]
do
  echo ${colors[$index]}
  let "index = $index + 1"
done
# Each array element listed on a separate line.
# If this is not desired, use  echo -n "${colors[$index]} "
#
# Doing it with a "for" loop instead:
#   for i in "${colors[@]}"
#   do echo "$i"
#   done
# (Thanks, S.C.)

echo

# Again, list all the elements in the array, but using a more elegant method.
  echo ${colors[@]}
# echo ${colors[*]} works also.


echo

exit 0
