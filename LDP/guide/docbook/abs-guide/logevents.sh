#!/bin/bash
# logevents.sh
# Author: Stephane Chazelas.
# Used in ABS Guide with permission.

# Event logging to a file.
# Must be run as root (for write access in /var/log).

ROOT_UID=0     # Only users with $UID 0 have root privileges.
E_NOTROOT=67   # Non-root exit error.


if [ "$UID" -ne "$ROOT_UID" ]
then
  echo "Must be root to run this script."
  exit $E_NOTROOT
fi  


FD_DEBUG1=3
FD_DEBUG2=4
FD_DEBUG3=5

# === Uncomment one of the two lines below to activate script. ===
# LOG_EVENTS=1
# LOG_VARS=1


log()  # Writes time and date to log file.
{
echo "$(date)  $*" &gt;&amp;7     # This *appends* the date to the file.
#     ^^^^^^^  command substitution
                           # See below.
}



case $LOG_LEVEL in
 1) exec 3&gt;&amp;2         4&gt; /dev/null 5&gt; /dev/null;;
 2) exec 3&gt;&amp;2         4&gt;&amp;2         5&gt; /dev/null;;
 3) exec 3&gt;&amp;2         4&gt;&amp;2         5&gt;&amp;2;;
 *) exec 3&gt; /dev/null 4&gt; /dev/null 5&gt; /dev/null;;
esac

FD_LOGVARS=6
if [[ $LOG_VARS ]]
then exec 6&gt;&gt; /var/log/vars.log
else exec 6&gt; /dev/null                     # Bury output.
fi

FD_LOGEVENTS=7
if [[ $LOG_EVENTS ]]
then
  # exec 7 &gt;(exec gawk '{print strftime(), $0}' &gt;&gt; /var/log/event.log)
  # Above line fails in versions of Bash more recent than 2.04. Why?
  exec 7&gt;&gt; /var/log/event.log              # Append to "event.log".
  log                                      # Write time and date.
else exec 7&gt; /dev/null                     # Bury output.
fi

echo "DEBUG3: beginning" &gt;&amp;${FD_DEBUG3}

ls -l &gt;&amp;5 2&gt;&amp;4                             # command1 &gt;&amp;5 2&gt;&amp;4

echo "Done"                                # command2 

echo "sending mail" &gt;&amp;${FD_LOGEVENTS}
# Writes "sending mail" to file descriptor #7.


exit 0
