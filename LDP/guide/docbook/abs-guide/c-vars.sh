#!/bin/bash
# Manipulating a variable, C-style, using the ((...)) construct.


echo

(( a = 23 ))  # Setting a value, C-style, with spaces on both sides of the "=".
echo "a (initial value) = $a"

(( a++ ))     # Post-increment 'a', C-style.
echo "a (after a++) = $a"

(( a-- ))     # Post-decrement 'a', C-style.
echo "a (after a--) = $a"


(( ++a ))     # Pre-increment 'a', C-style.
echo "a (after ++a) = $a"

(( --a ))     # Pre-decrement 'a', C-style.
echo "a (after --a) = $a"

echo

(( t = a<45?7:11 ))   # C-style trinary operator.
echo "If a < 45, then t = 7, else t = 11."
echo "t = $t "        # Yes!

echo


# -----------------
# Easter Egg alert!
# -----------------
#  Chet Ramey apparently snuck a bunch of undocumented C-style constructs
#+ into Bash (actually adapted from ksh, pretty much).
#  In the Bash docs, Ramey calls ((...)) shell arithmetic,
#+ but it goes far beyond that.
#  Sorry, Chet, the secret is now out.

# See also "for" and "while" loops using the ((...)) construct.

# These work only with Bash, version 2.04 or later.

exit 0
