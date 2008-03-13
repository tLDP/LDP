#!/bin/bash
# ascii.sh

# Script by Sebastian Arming.
# Lightly modified by ABS Guide author.
# Used with permission (thanks!).

exec >ASCII.txt         #  Save stdout to file,
                        #+ as in the example scripts
                        #+ reassign-stdout.sh and upperconv.sh.

MAXNUM=256
COLUMNS=5
OCT=8
OCTSQU=64
LITTLESPACE=-3
BIGSPACE=-5

i=1 # Decimal counter
o=1 # Octal counter

while [ "$i" -lt "$MAXNUM" ]; do
        paddi="    $i"
        echo -n "${paddi: $BIGSPACE}  "    # Column spacing.
        paddo="00$o"
        echo -ne "\\${paddo: $LITTLESPACE}"
        echo -n "     "
        if (( i % $COLUMNS == 0)); then    # New line.
           echo
        fi
        ((i++, o++))
        # The octal notation for 8 is 10 and 80 -> 100.
        (( i % $OCT == 0))    && ((o+=2))
        (( i % $OCTSQU == 0)) && ((o+=20))
        # We don't have to count past 0777.
done

exit 0
