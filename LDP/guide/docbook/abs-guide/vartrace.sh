#!/bin/bash

trap 'echo "VARIABLE-TRACE> \$variable = \"$variable\""' DEBUG
# Echoes the value of $variable after every command.

variable=29

echo "Just initialized \"\$variable\" to $variable."

let "variable *= 3"
echo "Just multiplied \"\$variable\" by 3."

# The "trap 'commands' DEBUG" construct would be more useful
# in the context of a complex script,
# where placing multiple "echo $variable" statements might be
# clumsy and time-consuming.

# Thanks, Stephane Chazelas for the pointer.

exit 0
