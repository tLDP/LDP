#!/bin/bash
# Escaped characters

echo "\v\v\v\v"      # Prints \v\v\v\v
# Must use the -e option with 'echo' to print escaped characters.
echo -e "\v\v\v\v"   # Prints 4 vertical tabs.
echo -e "\042"   # Prints " (quote, octal ASCII character 42).


# Bash, version 2 and later, permits using the $'\xxx' construct.
echo $'\n'
echo $'\a'
echo $'\t \042 \t'  # Quote (") framed by tabs.

# Assigning ASCII characters to a variable.
# ----------------------------------------
quote=$'\042'  # " assigned to a variable.
echo "$quote This is a quoted string, $quote and this lies outside the quotes."
# Concatenating ASCII chars in a variable.
triple_underline=$'\137\137\137'  # 137 is octal ASCII code for _
echo "$triple_underline UNDERLINE $triple_underline"

exit 0
