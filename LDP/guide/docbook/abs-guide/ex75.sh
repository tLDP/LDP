#!/bin/bash

#  This script is supposed to delete all filenames in current directory
#+ containing embedded spaces.
#  It doesn't work.
#  Why not?


badname=`ls | grep ' '`

# Try this:
# echo "$badname"

rm "$badname"

exit 0
