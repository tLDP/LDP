#!/bin/bash
# Killing ppp to force a log-off.

# Script should be run as root user.

killppp="eval kill -9 `ps ax | awk '/ppp/ { print $1 }'`"
#                     -------- process ID of ppp -------  

$killppp                  # This variable is now a command.


# The following operations must be done as root user.

chmod 666 /dev/ttyS3      # Must be read+write permissions, or else?
#  Since doing a SIGKILL on ppp changed the permissions on the serial port,
#+ we restore permissions to previous state.

rm /var/lock/LCK..ttyS3   # Remove the serial port lock file. Why?

exit 0

# Exercises:
# ---------
# 1) Have script check whether root user is invoking it.
# 2) Do a check on whether the process to be killed
#+   is actually running before attempting to kill it.   
