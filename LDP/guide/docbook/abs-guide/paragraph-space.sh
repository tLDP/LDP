#!/bin/bash
# paragraph-space.sh
# Ver. 2.0, Reldate 05Aug08

# Inserts a blank line between paragraphs of a single-spaced text file.
# Usage: $0 &lt;FILENAME

MINLEN=60        # May need to change this value.
#  Assume lines shorter than $MINLEN characters ending in a period
#+ terminate a paragraph. See exercises at end of script.

while read line  # For as many lines as the input file has...
do
  echo "$line"   # Output the line itself.

  len=${#line}
  if [[ "$len" -lt "$MINLEN" && "$line" =~ \[*\.\] ]]
    then echo    #  Add a blank line immediately
  fi             #+ after short line terminated by a period.
done

exit

# Exercises:
# ---------
#  1) The script usually inserts a blank line at the end
#+    of the target file. Fix this.
#  2) Line 17 only considers periods as sentence terminators.
#     Modify this to include other common end-of-sentence characters,
#+    such as ?, !, and ".
