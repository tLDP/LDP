#!/bin/bash

# This is supposed to delete all filenames
# containing embedded spaces in current directory,
# but doesn't.  Why not?


badname=`ls | grep ' '`

# echo "$badname"

rm "$badname"

exit 0
