#!/bin/bash
# Testing ranges of characters.

echo; echo "Hit a key, then hit return."
read Keypress

case "$Keypress" in
  [[:lower:]]   ) echo "Lowercase letter";;
  [[:upper:]]   ) echo "Uppercase letter";;
  [0-9]         ) echo "Digit";;
  *             ) echo "Punctuation, whitespace, or other";;
esac      #  Allows ranges of characters in [square brackets],
          #+ or POSIX ranges in [[double square brackets.

#  In the first version of this example,
#+ the tests for lowercase and uppercase characters were
#+ [a-z] and [A-Z].
#  This no longer works in certain locales and/or Linux distros.
#  POSIX is more portable.
#  Thanks to Frank Wang for pointing this out.

#  Exercise:
#  --------
#  As the script stands, it accepts a single keystroke, then terminates.
#  Change the script so it accepts repeated input,
#+ reports on each keystroke, and terminates only when "X" is hit.
#  Hint: enclose everything in a "while" loop.

exit 0
