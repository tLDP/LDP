#!/bin/bash
# erase.sh: Using "stty" to set an erase character when reading input.

echo -n "What is your name? "
read name                      # Try to erase characters of input.
                               # Won't work.
echo "Your name is $name."

stty erase '#'                 # Set "hashmark" (#) as erase character.
echo -n "What is your name? "
read name                      # Use # to erase last character typed.
echo "Your name is $name."

exit 0
