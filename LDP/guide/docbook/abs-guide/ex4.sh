#!/bin/bash

#  "subst", a script that substitutes one pattern for
#+ another in a file,
#+ i.e., "subst Smith Jones letter.txt".

ARGS=3         # Script requires 3 arguments.
E_BADARGS=65   # Wrong number of arguments passed to script.

if [ $# -ne "$ARGS" ]
# Test number of arguments to script (always a good idea).
then
  echo "Usage: `basename $0` old-pattern new-pattern filename"
  exit $E_BADARGS
fi

old_pattern=$1
new_pattern=$2

if [ -f "$3" ]
then
    file_name=$3
else
    echo "File \"$3\" does not exist."
    exit $E_BADARGS
fi


#  Here is where the heavy work gets done.

# -----------------------------------------------
sed -e "s/$old_pattern/$new_pattern/g" $file_name
# -----------------------------------------------

#  's' is, of course, the substitute command in sed,
#+ and /pattern/ invokes address matching.
#  The "g", or global flag causes substitution for *every*
#+ occurence of $old_pattern on each line, not just the first.
#  Read the literature on 'sed' for an in-depth explanation.

exit 0    # Successful invocation of the script returns 0.
