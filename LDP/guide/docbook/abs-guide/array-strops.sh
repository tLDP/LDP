#!/bin/bash
# array-strops.sh: String operations on arrays.
# Script by Michael Zick.
# Used with permission.

#  In general, any string operation in the ${name ... } notation
#+ can be applied to all string elements in an array
#+ with the ${name[@] ... } or ${name[*] ...} notation.


arrayZ=( one two three four five five )

echo

# Trailing Substring Extraction
echo ${arrayZ[@]:0}     # one two three four five five
                        # All elements.

echo ${arrayZ[@]:1}     # two three four five five
                        # All elements following element[0].

echo ${arrayZ[@]:1:2}   # two three
                        # Only the two elements after element[0].

echo "-----------------------"

#  Substring Removal
#  Removes shortest match from front of string(s),
#+ where the substring is a regular expression.

echo ${arrayZ[@]#f*r}   # one two three five five
                        # Applied to all elements of the array.
                        # Matches "four" and removes it.

# Longest match from front of string(s)
echo ${arrayZ[@]##t*e}  # one two four five five
                        # Applied to all elements of the array.
                        # Matches "three" and removes it.

# Shortest match from back of string(s)
echo ${arrayZ[@]%h*e}   # one two t four five five
                        # Applied to all elements of the array.
                        # Matches "hree" and removes it.

# Longest match from back of string(s)
echo ${arrayZ[@]%%t*e}  # one two four five five
                        # Applied to all elements of the array.
                        # Matches "three" and removes it.

echo "-----------------------"

# Substring Replacement

# Replace first occurance of substring with replacement
echo ${arrayZ[@]/fiv/XYZ}   # one two three four XYZe XYZe
                            # Applied to all elements of the array.

# Replace all occurances of substring
echo ${arrayZ[@]//iv/YY}    # one two three four fYYe fYYe
                            # Applied to all elements of the array.

# Delete all occurances of substring
# Not specifing a replacement means 'delete'
echo ${arrayZ[@]//fi/}      # one two three four ve ve
                            # Applied to all elements of the array.

# Replace front-end occurances of substring
echo ${arrayZ[@]/#fi/XY}    # one two three four XYve XYve
                            # Applied to all elements of the array.

# Replace back-end occurances of substring
echo ${arrayZ[@]/%ve/ZZ}    # one two three four fiZZ fiZZ
                            # Applied to all elements of the array.

echo ${arrayZ[@]/%o/XX}     # one twXX three four five five
                            # Why?

echo "-----------------------"


# Before reaching for awk (or anything else) --
# Recall:
#   $( ... ) is command substitution.
#   Functions run as a sub-process.
#   Functions write their output to stdout.
#   Assignment reads the function's stdout.
#   The name[@] notation specifies a "for-each" operation.

newstr() {
    echo -n "!!!"
}

echo ${arrayZ[@]/%e/$(newstr)}
# on!!! two thre!!! four fiv!!! fiv!!!
# Q.E.D: The replacement action is an 'assignment.'

#  Accessing the "For-Each"
echo ${arrayZ[@]//*/$(newstr optional_arguments)}
#  Now, if Bash would just pass the matched string as $0
#+ to the function being called . . .

echo

exit 0
