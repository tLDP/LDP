#!/bin/bash

# Delete filenames in current directory containing bad characters.

for filename in *
do
badname=`echo "$filename" | sed -n /[\+\{\;\"\\\=\?~\(\)\<\>\&\*\|\$]/p`
# Files containing those nasties:   + { ; " \ = ? ~ ( ) < > & * | $
rm $badname 2>/dev/null
#           So error messages deep-sixed.
done

# Now, take care of files containing all manner of whitespace.
find . -name "* *" -exec rm -f {} \;
# The "{}" references the paths of all the files that "find" finds.
# The '\' ensures that the ';' is interpreted literally, as end of command.

exit 0
