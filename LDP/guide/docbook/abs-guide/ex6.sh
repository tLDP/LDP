#!/bin/bash

# Check some of the system's environmental variables.
#  If, for example, $USER, the name of the person at the console, is not set,
#+ the machine will not recognize you.

: ${HOSTNAME?} ${USER?} ${HOME?} ${MAIL?}
  echo
  echo "Name of the machine is $HOSTNAME."
  echo "You are $USER."
  echo "Your home directory is $HOME."
  echo "Your mail INBOX is located in $MAIL."
  echo
  echo "If you are reading this message,"
  echo "critical environmental variables have been set."
  echo
  echo

# ------------------------------------------------------

#  The ${variablename?} construction can also check
#+ for variables set within the script.

ThisVariable=Value-of-ThisVariable
#  Note, by the way, that string variables may be set
#+ to characters disallowed in their names.
: ${ThisVariable?}
echo "Value of ThisVariable is $ThisVariable".
echo
echo


: ${ZZXy23AB?"ZZXy23AB has not been set."}
#  If ZZXy23AB has not been set,
#+ then the script terminates with an error message.

# You can specify the error message.
# : ${ZZXy23AB?"ZZXy23AB has not been set."}


# Same result with:    dummy_variable=${ZZXy23AB?}
#                      dummy_variable=${ZZXy23AB?"ZXy23AB has not been set."}
#
#                      echo ${ZZXy23AB?} >/dev/null



echo "You will not see this message, because script terminated above."

HERE=0
exit $HERE   # Will *not* exit here.
