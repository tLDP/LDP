#!/bin/bash
# du.sh: DOS to UNIX text file converter.

E_WRONGARGS=65

if [ -z "$1" ]
then
  echo "Usage: `basename $0` filename-to-convert"
  exit $E_WRONGARGS
fi

NEWFILENAME=$1.unx

CR='\015'  # Carriage return.
# Lines in a DOS text file end in a CR-LF.

tr -d $CR &lt; $1 &gt; $NEWFILENAME
# Delete CR and write to new file.

echo "Original DOS text file is \"$1\"."
echo "Converted UNIX text file is \"$NEWFILENAME\"."

exit 0
