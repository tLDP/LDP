#!/bin/bash

#When is a variable "naked", i.e., lacking the '$' in front?

# Assignment
a=879
echo $a

# Assignment using 'let'
let a=16+5
echo $a

# In a 'for' loop (really, a type of disguised assignment)
for a in 7 8 9 11
do
  echo $a
done

exit 0
