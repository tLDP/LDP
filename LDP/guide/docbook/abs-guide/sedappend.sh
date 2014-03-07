#!/bin/bash
#  Prepends a string at a specified line
#+ in files with names ending in "sample"
#+ in the current working directory.
#  000000000000000000000000000000000000
#  This script overwrites files!
#  Be careful running it in a directory
#+ where you have important files!!!
#  000000000000000000000000000000000000

#  Create a couple of files to operate on ...
#  01sample
#  02sample
#  ... etc.
#  These files must not be empty, else the prepend will not work.

lineno=1            # Append at line 1 (prepend).
filespec="*sample"  # Filename pattern to operate on.

string=$(whoami)    # Will set your username as string to insert.
                    # It could just as easily be any other string.

for file in $filespec # Specify which files to alter.
do #        ^^^^^^^^^
 sed -i ""$lineno"i "$string"" $file
#    ^^ -i option edits files in-place.
#                 ^ Insert (i) command.
 echo ""$file" altered!"
done

echo "Warning: files possibly clobbered!"

exit 0

# Exercise:
# Add error checking to this script.
# It needs it badly.
