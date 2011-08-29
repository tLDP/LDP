#!/bin/bash
# exercising-dd.sh

# Script by Stephane Chazelas.
# Somewhat modified by ABS Guide author.

infile=$0           # This script.
outfile=log.txt     # Output file left behind.
n=8
p=11

dd if=$infile of=$outfile bs=1 skip=$((n-1)) count=$((p-n+1)) 2> /dev/null
# Extracts characters n to p (8 to 11) from this script ("bash").

# ----------------------------------------------------------------

echo -n "hello vertical world" | dd cbs=1 conv=unblock 2> /dev/null
# Echoes "hello vertical world" vertically downward.
# Why? A newline follows each character dd emits.

exit $?
