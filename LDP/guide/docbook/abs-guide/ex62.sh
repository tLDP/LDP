#!/bin/bash

func ()
{
  local loc_var=23       # Declared local.
  echo
  echo "\"loc_var\" in function = $loc_var"
  global_var=999         # Not declared local.
  echo "\"global_var\" in function = $global_var"
}  

func

# Now, see if local 'a' exists outside function.

echo
echo "\"loc_var\" outside function = $loc_var"
                                      # "loc_var" outside function = 
                                      # Nope, $loc_var not visible globally.
echo "\"global_var\" outside function = $global_var"
                                      # "global_var" outside function = 999
                                      # $global_var is visible globally.
echo				      

exit 0
