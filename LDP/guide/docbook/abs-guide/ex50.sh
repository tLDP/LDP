#!/bin/bash

# Get a file listing...

b=`ls /usr/local/bin`

echo $b | fmt -w 40   # ...40 columns wide.

# Could also have been done by
#  echo $b | fold - -s -w 40
 
exit 0
