#!/bin/bash
# escaped.sh: escaped characters

echo; echo

echo "\v\v\v\v"      # Prints \v\v\v\v
# Use the -e option with 'echo' to print escaped characters.
echo -e "\v\v\v\v"   # Prints 4 vertical tabs.
echo -e "\042"       # Prints " (quote, octal ASCII character 42).

# The $'\X' construct makes the -e option unnecessary.
echo $'\n'           # Newline.
echo $'\a'           # Alert (beep).

# Version 2 and later of Bash permits using the $'\xxx' construct.
echo $'\t \042 \t'   # Quote (") framed by tabs.


# Assigning ASCII characters to a variable.
# ----------------------------------------
quote=$'\042'        # " assigned to a variable.
echo "$quote This is a quoted string, $quote and this lies outside the quotes."

echo

# Concatenating ASCII chars in a variable.
triple_underline=$'\137\137\137'  # 137 is octal ASCII code for '_'.
echo "$triple_underline UNDERLINE $triple_underline"

ABC=$'\101\102\103\010'           # 101, 102, 103 are octal A, B, C.
echo $ABC

echo; echo

escape=$'\033'                    # 033 is octal for escape.
echo "\"escape\" echoes as $escape"
#                                   no visible output.

echo; echo

exit 0
