#!/bin/bash

echo -n "Enter the value of variable 'var1': "
# -n option to echo suppresses newline

read var1
# Note no '$' in front of var1,
# since it is being set.

echo "var1 = $var1"

exit 0
