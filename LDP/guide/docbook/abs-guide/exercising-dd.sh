#!/bin/bash
# exercising-dd.sh

# Script by Stephane Chazelas.
# Somewhat modified by document author.

input_file=$0   # This script.
output_file=log.txt
n=3
p=5

dd if=$input_file of=$output_file bs=1 skip=$((n-1)) count=$((p-n+1)) 2> /dev/null
# Extracts characters n to p from this script.

# -------------------------------------------------------

echo -n "hello world" | dd cbs=1 conv=unblock 2> /dev/null
# Echoes "hello world" vertically.

exit 0
