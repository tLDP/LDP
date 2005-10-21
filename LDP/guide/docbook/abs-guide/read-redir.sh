#!/bin/bash

read var1 &lt;data-file
echo "var1 = $var1"
# var1 set to the entire first line of the input file "data-file"

read var2 var3 &lt;data-file
echo "var2 = $var2   var3 = $var3"
# Note non-intuitive behavior of "read" here.
# 1) Rewinds back to the beginning of input file.
# 2) Each variable is now set to a corresponding string,
#    separated by whitespace, rather than to an entire line of text.
# 3) The final variable gets the remainder of the line.
# 4) If there are more variables to be set than whitespace-terminated strings
#    on the first line of the file, then the excess variables remain empty.

echo "------------------------------------------------"

# How to resolve the above problem with a loop:
while read line
do
  echo "$line"
done &lt;data-file
# Thanks, Heiner Steven for pointing this out.

echo "------------------------------------------------"

# Use $IFS (Internal Field Separator variable) to split a line of input to
# "read", if you do not want the default to be whitespace.

echo "List of all users:"
OIFS=$IFS; IFS=:       # /etc/passwd uses ":" for field separator.
while read name passwd uid gid fullname ignore
do
  echo "$name ($fullname)"
done &lt;/etc/passwd   # I/O redirection.
IFS=$OIFS              # Restore original $IFS.
# This code snippet also by Heiner Steven.



#  Setting the $IFS variable within the loop itself
#+ eliminates the need for storing the original $IFS
#+ in a temporary variable.
#  Thanks, Dim Segebart, for pointing this out.
echo "------------------------------------------------"
echo "List of all users:"

while IFS=: read name passwd uid gid fullname ignore
do
  echo "$name ($fullname)"
done &lt;/etc/passwd   # I/O redirection.

echo
echo "\$IFS still $IFS"

exit 0
