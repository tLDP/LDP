#!/bin/bash

echo hello
echo $?
# exit status 0 returned
# because command successful.

lskdf
# bad command
echo $?
# non-zero exit status returned.

echo

exit 143
# Will return 143 to shell.
# To verify this, type $? after script terminates.

# By convention, an 'exit 0' shows success,
# while a non-zero exit value indicates an error.
