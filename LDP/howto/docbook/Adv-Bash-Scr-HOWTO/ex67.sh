#!/bin/bash

declare -a colors
# Permits declaring an array without specifying size.

echo "Enter your favorite colors (separated from each other by a space)."

read -a colors
# Special option to 'read' command,
# allowing it to assign elements in an array.

echo

element_count=${#colors[@]}
# Special syntax to extract number of elements in array.
index=0

while [ $index -lt $element_count ]
do
  echo ${colors[$index]}
  let "index = $index + 1"
done

echo

exit 0
