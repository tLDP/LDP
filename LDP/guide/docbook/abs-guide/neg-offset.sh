#!/bin/bash
# Bash, version -ge 4.2
# Negative length-index in substring extraction.
# Important: It changes the interpretation of this construct!

stringZ=abcABC123ABCabc

echo ${stringZ}                              # abcABC123ABCabc
#                   Position within string:    0123456789.....
echo ${stringZ:2:3}                          #   cAB
#  Count 2 chars forward from string beginning, and extract 3 chars.
#  ${string:position:length}

#  So far, nothing new, but now ...

                                             # abcABC123ABCabc
#                   Position within string:    0123....6543210
echo ${stringZ:3:-6}                         #    ABC123
#                ^
#  Index 3 chars forward from beginning and 6 chars backward from end,
#+ and extract everything in between.
#  ${string:offset-from-front:offset-from-end}
#  When the "length" parameter is negative, 
#+ it serves as an offset-from-end parameter.

#  See also neg-array.sh.
