#!/bin/bash

echo; echo "Hit a key, then hit return."
read Keypress

case "$Keypress" in
  [a-z]   ) echo "Lowercase letter";;
  [A-Z]   ) echo "Uppercase letter";;
  [0-9]   ) echo "Digit";;
  *       ) echo "Punctuation, whitespace, or other";;
esac  # Allows ranges of characters in [square brackets].

# Exercise:
# --------
# As the script stands, # it accepts a single keystroke, then terminates.
# Change the script so it accepts continuous input,
# reports on each keystroke, and terminates only when "X" is hit.
# Hint: enclose everything in a "while" loop.

exit 0
