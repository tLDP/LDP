#!/bin/bash
# Same as previous example, but with "until" loop.

if [ -z "$1" ]
then
  Filename=names.data         # Default, if no filename specified.
else
  Filename=$1
fi  

# while [ "$name" != Smith ]
until [ "$name" = Smith ]     # Change  !=  to =.
do
  read name                   # Reads from $Filename, rather than stdin.
  echo $name
done &lt;"$Filename"             # Redirects stdin to file $Filename. 
#    ^^^^^^^^^^^^

# Same results as with "while" loop in previous example.

exit 0
