#!/bin/bash
# Arithmetic tests.

# The (( )) construct evaluates and tests numerical expressions.

(( 0 ))
echo "Exit status of \"(( 0 ))\" is $?."

(( 1 ))
echo "Exit status of \"(( 1\ ))" is $?."

exit 0
