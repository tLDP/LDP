#!/bin/bash

echo
echo "Hit a key, then hit return."
read Keypress

case "$Keypress" in
  [a-z]   ) echo "Lowercase letter";;
  [A-Z]   ) echo "Uppercase letter";;
  [0-9]   ) echo "Digit";;
  *       ) echo "Punctuation, whitespace, or other";;
esac
# Allows ranges of characters in [square brackets].

exit 0
