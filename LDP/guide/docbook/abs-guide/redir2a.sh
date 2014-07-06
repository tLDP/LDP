#!/bin/bash

# This is an alternate form of the preceding script.

#  Suggested by Heiner Steven
#+ as a workaround in those situations when a redirect loop
#+ runs as a subshell, and therefore variables inside the loop
# +do not keep their values upon loop termination.


if [ -z "$1" ]
then
  Filename=names.data     # Default, if no filename specified.
else
  Filename=$1
fi  


exec 3&lt;&amp;0                 # Save stdin to file descriptor 3.
exec 0&lt;"$Filename"        # Redirect standard input.

count=0
echo


while [ "$name" != Smith ]
do
  read name               # Reads from redirected stdin ($Filename).
  echo $name
  let "count += 1"
done                      #  Loop reads from file $Filename
                          #+ because of line 20.

#  The original version of this script terminated the "while" loop with
#+      done &lt;"$Filename" 
#  Exercise:
#  Why is this unnecessary?


exec 0&lt;&amp;3                 # Restore old stdin.
exec 3&lt;&amp;-                 # Close temporary fd 3.

echo; echo "$count names read"; echo

exit 0
