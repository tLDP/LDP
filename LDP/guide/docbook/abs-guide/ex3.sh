#!/bin/bash

# This is a simple script that removes blank lines from a file.
# No argument checking.

# Same as
#    sed -e '/^$/d' filename
# invoked from the command line.

sed -e /^$/d "$1"
# The '-e' means an "editing" command follows (optional here).
# '^' is beginning of line,
# '$' is end,
# and 'd' is delete.
# Quoting the command-line arg permits special chars in the filename.

exit 0
