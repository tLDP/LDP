#!/bin/bash
#  Generic shell wrapper that performs an operation
#+ and logs it.

# Must set the following two variables.
OPERATION=
#         Can be a complex chain of commands,
#+        for example an awk script or a pipe . . .
LOGFILE=
#         Command-line arguments, if any, for the operation.


OPTIONS="$@"


# Log it.
echo "`date` + `whoami` + $OPERATION "$@"" >> $LOGFILE
# Now, do it.
exec $OPERATION "$@"

# It's necessary to do the logging before the operation.
# Why?
