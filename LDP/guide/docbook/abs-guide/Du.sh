#!/bin/bash
# Du.sh: DOS to UNIX text file converter.

E_WRONGARGS=85

if [ -z "$1" ]
then
  echo "Usage: `basename $0` filename-to-convert"
  exit $E_WRONGARGS
fi

NEWFILENAME=$1.unx

CR='\015'  # Carriage return.
           # 015 is octal ASCII code for CR.
           # Lines in a DOS text file end in CR-LF.
           # Lines in a UNIX text file end in LF only.

tr -d $CR &lt; $1 &gt; $NEWFILENAME
# Delete CR's and write to new file.

echo "Original DOS text file is \"$1\"."
echo "Converted UNIX text file is \"$NEWFILENAME\"."

exit 0

# Exercise:
# --------
# Change the above script to convert from UNIX to DOS.
