#!/bin/bash

# Bubble sort, of sorts.

# Recall the algorithm for a bubble sort. In this particular version...

# With each successive pass through the array to be sorted,
# compare two adjacent elements, and swap them if out of order.
# At the end of the first pass, the "heaviest" element has sunk to bottom.
# At the end of the second pass, the next "heaviest" one has sunk next to bottom.
# And so forth.
# This means that each successive pass needs to traverse less of the array.
# You will therefore notice a speeding up in the printing of the later passes.


exchange()
{
  # Swaps two members of the array.
  local temp=${Countries[$1]} # Temporary storage for element getting swapped out.
  Countries[$1]=${Countries[$2]}
  Countries[$2]=$temp
  
  return
}  

declare -a Countries  # Declare array.

Countries=(Netherlands Ukraine Zair Turkey Russia Yemen Syria Brazil Argentina Nicaragua Japan Mexico Venezuela Greece England Israel Peru Canada Oman Denmark Wales France Kashmir Qatar Liechtenstein Hungary)
# Couldn't think of one starting with X (darn).

clear  # Clear the screen to start with. 

echo "0: ${Countries[*]}"  # List entire array at pass 0.

number_of_elements=${#Countries[@]}
let "comparisons = $number_of_elements - 1"

count=1 # Pass number.

while [ $comparisons -gt 0 ]   # Beginning of outer loop
do

  index=0  # Reset index to start of array after each pass.

  while [ $index -lt $comparisons ] # Beginning of inner loop
  do
    if [ ${Countries[$index]} \> ${Countries[`expr $index + 1`]} ]
    # If out of order...
    # Recalling that \> is ASCII comparison operator.
    then
      exchange $index `expr $index + 1`  # Swap.
    fi  
    let "index += 1"
  done # End of inner loop
  

let "comparisons -= 1"
# Since "heaviest" element bubbles to bottom, we need do one less comparison each pass.

echo
echo "$count: ${Countries[@]}"
# Print resultant array at end of each pass.
echo
let "count += 1"   # Increment pass count.

done  # End of outer loop

# All done.

exit 0
