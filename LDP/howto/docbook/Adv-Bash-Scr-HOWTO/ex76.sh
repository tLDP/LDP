#!/bin/bash

trap 'echo Variable Listing --- a = $a  b = $b' EXIT
# EXIT is the name of the signal generated
# upon exit from a script.

a=39

b=36

exit 0
# Note that commenting out the 'exit' command
# does not make a difference.
