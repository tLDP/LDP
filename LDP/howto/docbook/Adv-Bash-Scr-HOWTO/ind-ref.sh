#!/bin/bash

# Indirect variable referencing.


a=letter_of_alphabet
letter_of_alphabet=z

# Direct reference.
echo "a = $a"

# Indirect reference.
eval a=\$$a
echo "Now a = $a"

echo


# Now, let's try changing the second order reference.

t=table_cell_3
table_cell_3=24
eval t=\$$t
echo "t = $t"
# So far, so good.

table_cell_3=387
eval t=\$$t
echo "Value of t changed to $t"
# ERROR!
# Cannot indirectly reference changed value of variable this way.
# For this to work, must use ${!t} notation.


exit 0
