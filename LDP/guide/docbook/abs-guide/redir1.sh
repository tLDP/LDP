#!/bin/bash
# Redirecting stdin using 'exec'.


exec 6&lt;&amp;0          # Link file descriptor #6 with stdin.
                   # Saves stdin.

exec &lt; data-file   # stdin replaced by file "data-file"

read a1            # Reads first line of file "data-file".
read a2            # Reads second line of file "data-file."

echo
echo "Following lines read from file."
echo "-------------------------------"
echo $a1
echo $a2

echo; echo; echo

exec 0&lt;&amp;6 6&lt;&amp;-
#  Now restore stdin from fd #6, where it had been saved,
#+ and close fd #6 ( 6&lt;&amp;- ) to free it for other processes to use.
#
# &lt;&amp;6 6&lt;&amp;-    also works.

echo -n "Enter data  "
read b1  # Now "read" functions as expected, reading from normal stdin.
echo "Input read from stdin."
echo "----------------------"
echo "b1 = $b1"

echo

exit 0
