#!/bin/bash

# Indirect variable referencing.
# This has a few of the attributes of references in C++.


a=letter_of_alphabet
letter_of_alphabet=z

# Direct reference.
echo "a = $a"

# Indirect reference.
echo "Now a = ${!a}"

echo

t=table_cell_3
table_cell_3=24
echo "t = ${!t}"
table_cell_3=387
echo "Value of t changed to ${!t}"
# Useful for referencing members
# of an array or table,
# or for simulating a multi-dimensional array.
# An indexing option would have been nice (sigh).


exit 0
