#!/bin/bash
# subshell.sh

echo

outer_variable=Outer

(
inner_variable=Inner
echo "From subshell, \"inner_variable\" = $inner_variable"
echo "From subshell, \"outer\" = $outer_variable"
)

echo

if [ -z "$inner_variable" ]
then
  echo "inner_variable undefined in main body of shell"
else
  echo "inner_variable defined in main body of shell"
fi

echo "From main body of shell, \"inner_variable\" = $inner_variable"
# $inner_variable will show as uninitialized because
# variables defined in a subshell are "local variables".

echo

exit 0
