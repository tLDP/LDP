#!/bin/bash

# Invoke both with and without arguments,
# and see what happens.

for a
do
 echo $a
done

# 'in list' missing, therefore operates on '$@'
# (command-line argument list, including white space)

exit 0
