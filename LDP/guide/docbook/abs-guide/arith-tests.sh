#!/bin/bash
# Arithmetic tests.

# The (( ... )) construct evaluates and tests numerical expressions.
# Exit status opposite from [ ... ] construct!

(( 0 ))
echo "Exit status of \"(( 0 ))\" is $?."   # 1

(( 1 ))
echo "Exit status of \"(( 1 ))\" is $?."   # 0

(( 5 > 4 ))                                # true
echo $?                                    # 0

(( 5 > 9 ))                                # false
echo $?                                    # 1

exit 0
