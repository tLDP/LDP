#!/bin/bash

# Generates a log file in current directory
# from the tail end of /var/log/messages.

# Note: /var/log/messages must be world readable
# if this script invoked by an ordinary user.
#         #root chmod 644 /var/log/messages

LINES=5

( date; uname -a ) >>logfile
# Time and machine name
echo --------------------------------------------------------------------- >>logfile
tail -$LINES /var/log/messages | xargs |  fmt -s >>logfile
echo >>logfile
echo >>logfile

exit 0

# Exercise:
# --------
#  Modify this script to track changes in /var/log/messages at intervals
#+ of 20 minutes.
#  Hint: Use the "watch" command. 
