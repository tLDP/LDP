#!/bin/bash

# String expansion.
# Introduced in version 2 of bash.

# Strings of the form $'xxx'
# have the standard escaped characters interpreted. 

echo $'Ringing bell 3 times \a \a \a'
echo $'Three form feeds \f \f \f'
echo $'10 newlines \n\n\n\n\n\n\n\n\n\n'

exit 0
