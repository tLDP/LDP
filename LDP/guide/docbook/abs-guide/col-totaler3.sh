#!/bin/bash

#  Yet another version of the "column totaler" script (col-totaler.sh)
#+ that adds up a specified column (of numbers) in the target file.
#  This uses the environment to pass a script variable to 'awk'.

ARGS=2
E_WRONGARGS=65

if [ $# -ne "$ARGS" ] # Check for proper no. of command line args.
then
   echo "Usage: `basename $0` filename column-number"
   exit $E_WRONGARGS
fi

filename=$1
column_number=$2

#===== Same as original script, up to this point =====#

export column_number
# Export column number to environment, so it's available for retrieval.


# Begin awk script.
# ------------------------------------------------
awk '{ total += $ENVIRON["column_number"]
}
END { print total }' $filename
# ------------------------------------------------
# End awk script.


# Thanks, Stephane Chazelas.

exit 0
