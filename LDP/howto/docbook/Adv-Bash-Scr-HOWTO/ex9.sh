#!/bin/bash

a=37.5
hello=$a
# No space permitted on either side of = sign.

echo hello

echo $hello
echo ${hello} #Identical as above.

echo "$hello"
echo "${hello}"

echo '$hello'
# Variable referencing disabled by single quotes.

# Notice the effect of different
# types of quoting.

exit 0
