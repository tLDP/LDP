#!/bin/bash
# hexconvert.sh: Convert a decimal number to hexadecimal.

E_NOARGS=65 # Command-line arg missing.
BASE=16     # Hexadecimal.

if [ -z "$1" ]
then
  echo "Usage: $0 number"
  exit $E_NOARGS
  # Need a command line argument.
fi
# Exercise: add argument validity checking.


hexcvt ()
{
if [ -z "$1" ]
then
  echo 0
  return    # "Return" 0 if no arg passed to function.
fi

echo ""$1" "$BASE" o p" | dc
#                 "o" sets radix (numerical base) of output.
#                   "p" prints the top of stack.
# See 'man dc' for other options.
return
}

hexcvt "$1"

exit 0
