#!/bin/bash

# Generates a log file in current directory
# from the tail end of /var/log messages.

# Note: /var/log/messages must be readable by ordinary users
#       if invoked by same (#root chmod 755 /var/log/messages).

( date; uname -a ) >>logfile
# Time and machine name
echo --------------------------------------------------------------------- >>logfile
tail -5 /var/log/messages | xargs |  fmt -s >>logfile
echo >>logfile
echo >>logfile

exit 0
