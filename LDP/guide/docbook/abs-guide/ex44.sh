#!/bin/bash

y=`eval ps ax | sed -n '/ppp/p' | awk '{ print $1 }'`
# Finding the process number of 'ppp'.

kill -9 $y   # Killing it

# Above lines may be replaced by
#  kill -9 `ps ax | awk '/ppp/ { print $1 }'`


chmod 666 /dev/ttyS3
# Doing a SIGKILL on ppp changes the permissions
# on the serial port. Restore them to previous state.

rm /var/lock/LCK..ttyS3   # Remove the serial port lock file.

exit 0
