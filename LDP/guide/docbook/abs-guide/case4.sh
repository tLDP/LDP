#!/bin/bash4

test_char ()
{
  case "$1" in
    [[:print:]] )  echo "$1 is a printable character.";;&amp;       # |
    # The ;;&amp; terminator continues to the next pattern test.      |
    [[:alnum:]] )  echo "$1 is an alpha/numeric character.";;&amp;  # v
    [[:alpha:]] )  echo "$1 is an alphabetic character.";;&amp;     # v
    [[:lower:]] )  echo "$1 is a lowercase alphabetic character.";;&amp;
    [[:digit:]] )  echo "$1 is an numeric character.";&amp;         # |
    # The ;&amp; terminator executes the next statement ...         # |
    %%%@@@@@    )  echo "********************************";;    # v
#   ^^^^^^^^  ... even with a dummy pattern.
  esac
}

echo

test_char 3
# 3 is a printable character.
# 3 is an alpha/numeric character.
# 3 is an numeric character.
# ********************************
echo

test_char m
# m is a printable character.
# m is an alpha/numeric character.
# m is an alphabetic character.
# m is a lowercase alphabetic character.
echo

test_char /
# / is a printable character.

echo

# The ;;&amp; terminator can save complex if/then conditions.
# The ;&amp; is somewhat less useful.
