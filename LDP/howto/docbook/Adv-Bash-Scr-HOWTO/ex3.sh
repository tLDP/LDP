#!/bin/bash

# This is a simple script
# that removes blank lines
# from a file.
# No argument checking.

# Same as
# sed -e '/^$/d $1' filename
# invoked from the command line.

sed -e /^$/d $1
# '^' is beginning of line,
# '$' is end,
# and 'd' is delete.
