#!/bin/bash
# shft.sh: Using 'shift' to step through all the positional parameters

#  Name this script something like shft.sh,
#+ and invoke it with some parameters.
#+ For example:
#             sh shft.sh a b c def 23 skidoo

until [ -z "$1" ]  # Until all parameters used up . . .
do
  echo -n "$1 "
  shift
done

echo               # Extra line feed.

exit 0

#  See also the echo-params.sh script for a "shiftless"
#+ alternative method of stepping through the positional params.
