#!/bin/bash

# "subst", a script that substitutes one pattern for
# another in a file,
# i.e., "subst Smith Jones letter.txt".

if [ $# -ne 3 ]
# Test number of arguments to script
# (always a good idea).
then
  echo "Usage: `basename $0` old-pattern new-pattern filename"
  exit 1
fi

old_pattern=$1
new_pattern=$2

if [ -f $3 ]
then
    file_name=$3
else
    echo "File \"$3\" does not exist."
    exit 2
fi

# Here is where the heavy work gets done.
sed -e "s/$old_pattern/$new_pattern/" $file_name
# 's' is, of course, the substitute command in sed,
# and /pattern/ invokes address matching.
# Read the literature on 'sed' for a more
# in-depth explanation.

exit 0
# Successful invocation of the script returns 0.
