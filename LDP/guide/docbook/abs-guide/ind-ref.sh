#!/bin/bash
# Indirect variable referencing.

a=letter_of_alphabet
letter_of_alphabet=z

echo

# Direct reference.
echo "a = $a"

# Indirect reference.
eval a=\$$a
echo "Now a = $a"

echo


# Now, let's try changing the second order reference.

t=table_cell_3
table_cell_3=24
echo "\"table_cell_3\" = $table_cell_3"
echo -n "dereferenced \"t\" = "; eval echo \$$t
# In this simple case,
#   eval t=\$$t; echo "\"t\" = $t"
# also works (why?).

echo

t=table_cell_3
NEW_VAL=387
table_cell_3=$NEW_VAL
echo "Changing value of \"table_cell_3\" to $NEW_VAL."
echo "\"table_cell_3\" now $table_cell_3"
echo -n "dereferenced \"t\" now "; eval echo \$$t
# "eval" takes the two arguments "echo" and "\$$t" (set equal to $table_cell_3)
echo

# (Thanks, S.C., for clearing up the above behavior.)


# Another method is the ${!t} notation, discussed in "Bash, version 2" section.
# See also example "ex78.sh".

exit 0
