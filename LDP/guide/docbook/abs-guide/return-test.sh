#!/bin/bash
# return-test.sh

# The largest positive value a function can return is 256.

return_test ()         # Returns whatever passed to it.
{
  return $1
}

return_test 27         # o.k.
echo $?                # Returns 27.
  
return_test 256        # Still o.k.
echo $?                # Returns 256.

return_test 257        # Error!
echo $?                # Returns 1 (return code for miscellaneous error).

return_test -151896    # However, large negative numbers work.
echo $?                # Returns -151896.

exit 0
