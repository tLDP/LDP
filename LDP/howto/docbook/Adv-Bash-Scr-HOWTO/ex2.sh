#!/bin/bash
# cleanup, version 2
# Run as root, of course.

if [ -n $1 ]
# Test if command line argument present.
then
  lines=$1
else  
  lines=50
  # default, if not specified on command line.
fi  


cd /var/log
tail -$lines messages > mesg.temp
# Saves last section of message log file.
mv mesg.temp messages

# cat /dev/null > messages
# No longer needed, as the above method is safer.

cat /dev/null > wtmp
echo "Logs cleaned up."

exit 0
# A zero return value from the script upon exit
# indicates success to the shell.
