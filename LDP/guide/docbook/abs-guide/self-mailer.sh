#!/bin/sh
# self-mailer.sh: Self-mailing script

ARGCOUNT=1              # Need name of addressee.
E_WRONGARGS=65
if [ $# -ne "$ARGCOUNT" ]
then
  echo "Usage: `basename $0` addressee"
  exit $E_WRONGARGS
fi  

# ========================================================================
cat $0 | mail -s "Script \"`basename $0`\" has mailed itself to you." "$1"
# ========================================================================

# --------------------------------------------
#  Greetings from the self-mailing script.
#  A mischievous person has run this script,
#+ which has caused it to mail itself to you.
#  Apparently, some people have nothing better
#+ to do with their time.
# --------------------------------------------

exit 0
