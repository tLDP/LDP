#!/bin/bash

if [ -z "$1" ]
then
  Filename=names.data       # Default, if no filename specified.
else
  Filename=$1
fi  
#+ Filename=${1:-names.data}
#  can replace the above test (parameter substitution).

count=0

echo

while [ "$name" != Smith ]  # Why is variable $name in quotes?
do
  read name                 # Reads from $Filename, rather than stdin.
  echo $name
  let "count += 1"
done <"$Filename"           # Redirects stdin to file $Filename. 
#    ^^^^^^^^^^^^

echo; echo "$count names read"; echo

#  Note that in some older shell scripting languages,
#+ the redirected loop would run as a subshell.
# Therefore, $count would return 0, the initialized value outside the loop.
#  Bash and ksh avoid starting a subshell whenever possible,
# +so that this script, for example, runs correctly.
#
# Thanks to Heiner Steven for pointing this out.

exit 0
