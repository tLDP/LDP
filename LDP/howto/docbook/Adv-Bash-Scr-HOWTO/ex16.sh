#!/bin/bash

a=23
# Simple case
echo $a
b=$a
echo $b

# Now, getting a little bit fancier...

a=`echo Hello!`
# Assigns result of 'echo' command to 'a'
echo $a

a=`ls -l`
# Assigns result of 'ls -l' command to 'a'
echo $a

exit 0
