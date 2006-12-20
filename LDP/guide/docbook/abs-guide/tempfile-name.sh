#!/bin/bash
# tempfile-name.sh:  temp filename generator

BASE_STR=`mcookie`   # 32-character magic cookie.
POS=11               # Arbitrary position in magic cookie string.
LEN=5                # Get $LEN consecutive characters.

prefix=temp          #  This is, after all, a "temp" file.
                     #  For more "uniqueness," generate the
                     #+ filename prefix using the same method
                     #+ as the suffix, below.

suffix=${BASE_STR:POS:LEN}
                     #  Extract a 5-character string,
                     #+ starting at position 11.

temp_filename=$prefix.$suffix
                     # Construct the filename.

echo "Temp filename = "$temp_filename""

# sh tempfile-name.sh
# Temp filename = temp.e19ea

#  Compare this method of generating "unique" filenames
#+ with the 'date' method in ex51.sh.

exit 0
