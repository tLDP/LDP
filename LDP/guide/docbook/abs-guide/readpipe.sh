#!/bin/sh
# readpipe.sh
# This example contributed by Bjon Eriksson.

last="(null)"
cat $0 |
while read line
do
    echo "{$line}"
    last=$line
done
printf "\nAll done, last:$last\n"

exit 0  # End of code.
        # (Partial) output of script follows.
        # The 'echo' supplies extra brackets.

#############################################

./readpipe.sh 

{#!/bin/sh}
{last="(null)"}
{cat $0 |}
{while read line}
{do}
{echo "{$line}"}
{last=$line}
{done}
{printf "nAll done, last:$lastn"}


All done, last:(null)

The variable (last) is set within the subshell but unset outside.
