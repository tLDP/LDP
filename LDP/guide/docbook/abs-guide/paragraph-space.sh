#!/bin/bash
# paragraph-space.sh

# Inserts a blank line between paragraphs of a single-spaced text file.
# Usage: $0 &lt;FILENAME

MINLEN=45        # May need to change this value.
#  Assume lines shorter than $MINLEN characters
#+ terminate a paragraph.

while read line  # For as many lines as the input file has...
do
  echo "$line"   # Output the line itself.

  len=${#line}
  if [ "$len" -lt "$MINLEN" ]
    then echo    # Add a blank line after short line.
  fi  
done

exit 0
