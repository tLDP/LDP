#!/bin/bash

func ()
{
  local a=23
  echo
  echo "a in function = $a"
  echo
}  

func

# Now, see if local 'a' exists outside function.

echo "a outside function = $a"  # Nope, 'a' not visible globally.
echo

exit 0
