#!/bin/bash

a=23              # Simple case
echo $a
b=$a
echo $b

# Now, getting a little bit fancier (command substitution).

a=`echo Hello!`   # Assigns result of 'echo' command to 'a'
echo $a
#  Note that using an exclamation mark (!) in command substitution
#+ will not work from the command line,
#+ since this triggers the Bash "history mechanism."
#  Within a script, however, the history functions are disabled.

a=`ls -l`         # Assigns result of 'ls -l' command to 'a'
echo $a           # Unquoted, however, removes tabs and newlines.
echo
echo "$a"         # The quoted variable preserves whitespace.
                  # (See the chapter on "Quoting.")

exit 0
