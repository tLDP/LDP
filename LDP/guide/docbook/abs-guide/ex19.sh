#!/bin/bash
# Using 'shift' to step through all the positional parameters.

#  Name this script something like shft,
#+ and invoke it with some parameters, for example
#          ./shft a b c def 23 skidoo

until [ -z "$1" ]  # Until all parameters used up...
do
  echo -n "$1 "
  shift
done

echo               # Extra line feed.

exit 0
