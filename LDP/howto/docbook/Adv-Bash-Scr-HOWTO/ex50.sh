#!/bin/bash

# Get a file listing...

b=`ls /usr/local/bin`

# ...40 columns wide.
echo $b | fmt -w 40

# Could also have been done by
# echo $b | fold - -s -w 40
 
exit 0
