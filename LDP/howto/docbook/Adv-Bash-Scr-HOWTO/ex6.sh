#!/bin/bash

# Let's check some of the system's environmental variables.
# If, for example, $USER, the name of the person
# at the console, is not set, the machine will not
# recognize you.

: ${HOSTNAME?} ${USER?} ${HOME} ${MAIL?}
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

# The ':' operator seems fairly error tolerant.
# This script works even if the '$' omitted in front of
# {HOSTNAME}, {USER?}, {HOME?}, and {MAIL?}. Why?

# ------------------------------------------------------

# The ${variablename?} construction can also check
# for variables set within the script.

ThisVariable=Value-of-ThisVariable
# Note, by the way, that string variables may be set
# to characters disallowed in their names.
: ${ThisVariable?}
echo "Value of ThisVariable is $ThisVariable".
echo
echo

# If ZZXy23AB has not been set...
: ${ZZXy23AB?}
# This will give you an error message and terminate.

echo "You will not see this message."

exit 0 
