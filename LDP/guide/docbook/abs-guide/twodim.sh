#!/bin/bash
# Simulating a two-dimensional array.

# A two-dimensional array stores rows sequentially.

Rows=5
Columns=5

declare -a alpha     # char alpha [Rows] [Columns];
                     # Unnecessary declaration.

load_alpha ()
{
local rc=0
local index


for i in A B C D E F G H I J K L M N O P Q R S T U V W X Y
do
  local row=`expr $rc / $Columns`
  local column=`expr $rc % $Rows`
  let "index = $row * $Rows + $column"
  alpha[$index]=$i   # alpha[$row][$column]
  let "rc += 1"
done  

# Simpler would be
#   declare -a alpha=( A B C D E F G H I J K L M N O P Q R S T U V W X Y )
# but this somehow lacks the "flavor" of a two-dimensional array.
}

print_alpha ()
{
local row=0
local index

echo

while [ "$row" -lt "$Rows" ]   # Print out in "row major" order -
do                             # columns vary
                               # while row (outer loop) remains the same.
  local column=0
  
  while [ "$column" -lt "$Columns" ]
  do
    let "index = $row * $Rows + $column"
    echo -n "${alpha[index]} "  # alpha[$row][$column]
    let "column += 1"
  done

  let "row += 1"
  echo

done  

# The simpler equivalent is
#   echo ${alpha[*]} | xargs -n $Columns

echo
}

filter ()     # Filter out negative array indices.
{

echo -n "  "  # Provides the tilt.

if [[ "$1" -ge 0 &&  "$1" -lt "$Rows" && "$2" -ge 0 && "$2" -lt "$Columns" ]]
then
    let "index = $1 * $Rows + $2"
    # Now, print it rotated.
    echo -n " ${alpha[index]}"  # alpha[$row][$column]
fi    

}
  



rotate ()  # Rotate the array 45 degrees
{          # ("balance" it on its lower lefthand corner).
local row
local column

for (( row = Rows; row > -Rows; row-- ))  # Step through the array backwards.
do

  for (( column = 0; column < Columns; column++ ))
  do

    if [ "$row" -ge 0 ]
    then
      let "t1 = $column - $row"
      let "t2 = $column"
    else
      let "t1 = $column"
      let "t2 = $column + $row"
    fi  

    filter $t1 $t2   # Filter out negative array indices.
  done

  echo; echo

done 

# Array rotation inspired by examples (pp. 143-146) in
# "Advanced C Programming on the IBM PC", by Herbert Mayer
# (see bibliography).

}


#-----------------------------------------------------#
load_alpha     # Load the array.
print_alpha    # Print it out.  
rotate         # Rotate it 45 degrees counterclockwise.
#-----------------------------------------------------#


# This is a rather contrived, not to mention kludgy simulation.
#
# Exercises:
# ---------
# 1)  Rewrite the array loading and printing functions
#   + in a more intuitive and elegant fashion.
#
# 2)  Figure out how the array rotation functions work.
#     Hint: think about the implications of backwards-indexing an array.

exit 0
