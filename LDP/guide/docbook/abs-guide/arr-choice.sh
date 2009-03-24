#!/bin/bash
# arr-choice.sh

#  Passing arguments to a function to select
#+ one particular variable out of a group.

arr0=( 10 11 12 13 14 15 )
arr1=( 20 21 22 23 24 25 )
arr2=( 30 31 32 33 34 35 )
#       0  1  2  3  4  5      Element number (zero-indexed)


choose_array ()
{
  eval array_member=\${arr${array_number}[element_number]}
  #                 ^       ^^^^^^^^^^^^
  #  Using eval to construct the name of a variable,
  #+ in this particular case, an array name.

  echo "Element $element_number of array $array_number is $array_member"
} #  Function can be rewritten to take parameters.

array_number=0    # First array.
element_number=3
choose_array      # 13

array_number=2    # Third array.
element_number=4
choose_array      # 34

array_number=3    # Null array (arr3 not allocated).
element_number=4
choose_array      # (null)

# Thank you, Antonio Macchi, for pointing this out.
