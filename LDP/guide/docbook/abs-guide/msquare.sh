#!/bin/bash
# msquare.sh
# Magic Square generator (odd-order squares only!)

# Author: mendel cooper
# reldate: 19 Jan. 2009
# License: Public Domain
# A C-program by the very talented Kwon Young Shin inspired this script.
#     http://user.chollian.net/~brainstm/MagicSquare.htm

# Definition: A "magic square" is a two-dimensional array
#             of integers in which all the rows, columns,
#             and *long* diagonals add up to the same number.
#             Being "square," the array has the same number
#             of rows and columns. That number is the "order."
# An example of a magic square of order 3 is:
#   8  1  6   
#   3  5  7   
#   4  9  2   
# All the rows, columns, and the two long diagonals add up to 15.


# Globals
EVEN=2
MAXSIZE=31   # 31 rows x 31 cols.
E_usage=90   # Invocation error.
dimension=
declare -i square

usage_message ()
{
  echo "Usage: $0 order"
  echo "   ... where \"order\" (square size) is an ODD integer"
  echo "       in the range 3 - 31."
  #  Actually works for squares up to order 159,
  #+ but large squares will not display pretty-printed in a term window.
  #  Try increasing MAXSIZE, above.
  exit $E_usage
}


calculate ()       # Here's where the actual work gets done.
{
  local row col index dimadj j k cell_val=1
  dimension=$1

  let "dimadj = $dimension * 3"; let "dimadj /= 2"   # x 1.5, then truncate.

  for ((j=0; j &lt; dimension; j++))
  do
    for ((k=0; k &lt; dimension; k++))
    do  # Calculate indices, then convert to 1-dim. array index.
        # Bash doesn't support multidimensional arrays. Pity.
      let "col = $k - $j + $dimadj"; let "col %= $dimension"
      let "row = $j * 2 - $k + $dimension"; let "row %= $dimension"
      let "index = $row*($dimension) + $col"
      square[$index]=cell_val; ((cell_val++))
    done
  done
}     # Plain math, visualization not required.


print_square ()               # Output square, one row at a time.
{
  local row col idx d1
  let "d1 = $dimension - 1"   # Adjust for zero-indexed array.
 
  for row in $(seq 0 $d1)
  do

    for col in $(seq 0 $d1)
    do
      let "idx = $row * $dimension + $col"
      printf "%3d " "${square[idx]}"; echo -n "  "
    done   # Displays up to 13th order neatly in 80-column term window.

    echo   # Newline after each row.
  done
}


#################################################
if [[ -z "$1" ]] || [[ "$1" -gt $MAXSIZE ]]
then
  usage_message
fi

let "test_even = $1 % $EVEN"
if [ $test_even -eq 0 ]
then           # Can't handle even-order squares.
  usage_message
fi

calculate $1
print_square   # echo "${square[@]}"   # DEBUG

exit $?
#################################################


# Exercises:
# ---------
# 1) Add a function to calculate the sum of each row, column,
#    and *long* diagonal. The sums must match.
#    This is the "magic constant" of that particular order square.
# 2) Have the print_square function auto-calculate how much space
#    to allot between square elements for optimized display.
#    This might require parameterizing the "printf" line.
# 3) Add appropriate functions for generating magic squares
#    with an *even* number of rows/columns.
#    This is non-trivial(!).
#    See the URL for Kwon Young Shin, above, for help.
