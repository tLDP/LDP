#!/bin/bash

# Name this script something like shift000,
# and invoke it with some parameters, for example
# ./shift000 a b c def 23 skidoo

# Demo of using 'shift'
# to step through all the positional parameters.

until [ -z "$1" ]
do
  echo -n "$1 "
  shift
done

echo
# Extra line feed.

exit 0
