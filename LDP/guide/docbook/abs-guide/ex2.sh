#!/bin/bash
# cleanup, version 2
# Run as root, of course.

LOG_DIR=/var/log
ROOT_UID=0   # Only users with $UID 0 have root privileges.
LINES=50     # Default number of lines saved.
XCD=66       # Can't change directory?
NOTROOT=67   # Non-root exit error.


if [ "$UID" -ne "$ROOT_UID" ]
then
  echo "Must be root to run this script."
  exit $NOTROOT
fi  

if [ -n "$1" ]
# Test if command line argument present (non-empty).
then
  lines=$1
else  
  lines=$LINES
  # default, if not specified on command line.
fi  


# Stephane Chazelas suggests the following,
# as a better way of checking command line arguments,
# but this is still a bit advanced for this stage of the tutorial.
#
#    WRONGARGS=65  # Non-numerical argument (bad arg format)
#
#    case "$1" in
#    ""      ) lines=50;;
#    *[!0-9]*) echo "Usage: `basename $0` file-to-cleanup"; exit $WRONGARGS;;
#    *       ) lines=$1;;
#    esac
#
# Skip ahead to "Loops" to understand this.


cd $LOG_DIR

if [ `pwd` != "$LOG_DIR" ]  # or   if [ "$PWD" != "LOG_DIR" ]
# Not in /var/log?
then
  echo "Can't change to $LOG_DIR."
  exit $XCD
fi  # Doublecheck if in right directory, before messing with log file.

# far better is:
# ---
# cd /var/log || {
#   echo "Cannot change to necessary directory." >&2
#   exit $XCD;
# }




tail -$lines messages > mesg.temp # Saves last section of message log file.
mv mesg.temp messages  # Becomes new log directory.


# cat /dev/null > messages
# No longer needed, as the above method is safer.

cat /dev/null > wtmp  # > wtemp   has the same effect.
echo "Logs cleaned up."

exit 0
# A zero return value from the script upon exit
# indicates success to the shell.
