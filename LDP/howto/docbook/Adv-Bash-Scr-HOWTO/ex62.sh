#!/bin/bash

func ()
{
  local a=23
  echo
  echo "a in function is $a"
  echo
}  

func

# Now, see if local 'a'
# exists outside function.

echo "a outside function is $a"
echo
# Nope, 'a' not visible globally.

exit 0
