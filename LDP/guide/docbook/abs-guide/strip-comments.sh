#!/bin/bash

# Strips out the comments (/* comment */) in a C program.

NOARGS=0
ARGERROR=65
WRONG_FILE_TYPE=66

if [ $# -eq "$NOARGS" ]
then
  echo "Usage: `basename $0` C-program-file" >&2 # Error message to stderr.
  exit $ARGERROR
fi  

# Test for correct file type.
type=`eval file $1 | awk '{ print $2, $3, $4, $5 }'`
# "file $1" echoes file type...
# then awk removes the first field of this, the filename...
# then the result is fed into the variable "type".
correct_type="ASCII C program text"

if [ "$type" != "$correct_type" ]
then
  echo
  echo "This script works on C program files only."
  echo
  exit $WRONG_FILE_TYPE
fi  


# Rather cryptic sed script:
#--------
sed '
/^\/\*/d
/.*\/\*/d
' $1
#--------
# Easy to understand if you take several hours to learn sed fundamentals.


# Need to add one more line to the sed script to deal with
# case where line of code has a comment following it on same line.
# This is left as a non-trivial exercise for the reader.

# Also, the above code deletes lines with a "*/" or "/*",
# not a desirable result.

exit 0


# ----------------------------------------------------------------
# Code below this line will not execute because of 'exit 0' above.

# Stephane Chazelas suggests the following alternative:

usage() {
  echo "Usage: `basename $0` C-program-file" >&2
  exit 1
}

WEIRD=`echo -n -e '\377'`   # or WEIRD=$'\377'
[[ $# -eq 1 ]] || usage
case `file "$1"` in
  *"C program text"*) sed -e "s%/\*%${WEIRD}%g;s%\*/%${WEIRD}%g" "$1" \
     | tr '\377\n' '\n\377' \
     | sed -ne 'p;n' \
     | tr -d '\n' | tr '\377' '\n';;
  *) usage;;
esac

# This is still fooled by things like:
# printf("/*");
# or
# /*  /* buggy embedded comment */
#
# To handle all special cases (comments in strings, comments in string
# where there is a \", \\" ...) the only way is to write a C parser
# (lex or yacc perhaps?).

exit 0
