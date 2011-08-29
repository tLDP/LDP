#!/bin/bash
# userlist.sh

PASSWORD_FILE=/etc/passwd
n=1           # User number

for name in $(awk 'BEGIN{FS=":"}{print $1}' < "$PASSWORD_FILE" )
# Field separator = :    ^^^^^^
# Print first field              ^^^^^^^^
# Get input from password file               ^^^^^^^^^^^^^^^^^
do
  echo "USER #$n = $name"
  let "n += 1"
done  


# USER #1 = root
# USER #2 = bin
# USER #3 = daemon
# ...
# USER #30 = bozo

exit $?

#  Discussion:
#  ----------
#  How is it that an ordinary user, or a script run by same,
#+ can read /etc/passwd? (Hint: Check the /etc/passwd file permissions.)
#  Isn't this a security hole? Why or why not?
