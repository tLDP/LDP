#!/bin/bash
# exercising-dd.sh

# Script by Stephane Chazelas.
# Somewhat modified by ABS Guide author.

infile=$0       # This script.
outfile=log.txt # This output file left behind.
n=3
p=5

dd if=$infile of=$outfile bs=1 skip=$((n-1)) count=$((p-n+1)) 2> /dev/null
# Extracts characters n to p (3 to 5) from this script.

# --------------------------------------------------------

echo -n "hello world" | dd cbs=1 conv=unblock 2> /dev/null
# Echoes "hello world" vertically.
# Why? Newline after each character dd emits.

exit 0
