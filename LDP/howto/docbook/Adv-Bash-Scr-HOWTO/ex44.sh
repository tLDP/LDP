#!/bin/bash

y=`eval ps ax | sed -n '/ppp/p' | awk '{ print $1 }'`
# Finding the process number of 'ppp'

kill -9 $y
# Killing it


# Restore to previous state...

chmod 666 /dev/ttyS3
# Doing a SIGKILL on ppp changes the permissions
# on the serial port. Must be restored.

rm /var/lock/LCK..ttyS3
# Remove the serial port lock file.

exit 0
