#!/bin/bash
# Pitfalls of variables in a subshell.

outer_variable=outer
echo
echo "outer_variable = $outer_variable"
echo

(
# Begin subshell

echo "outer_variable inside subshell = $outer_variable"
inner_variable=inner  # Set
echo "inner_variable inside subshell = $inner_variable"
outer_variable=inner  # Will value change globally?
echo "outer_variable inside subshell = $outer_variable"

# End subshell
)

echo
echo "inner_variable outside subshell = $inner_variable"  # Unset.
echo "outer_variable outside subshell = $outer_variable"  # Unchanged.
echo

exit 0
