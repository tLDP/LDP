#!/bin/bash
# unset.sh: Unsetting a variable.

variable=hello                       # Initialized.
echo "variable = $variable"

unset variable                       # Uninitialized.
echo "(unset) variable = $variable"  # $variable is null.

exit 0
