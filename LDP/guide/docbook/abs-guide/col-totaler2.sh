#!/bin/bash

#  Another version of the "column totaler" script
#+ that adds up a specified column (of numbers) in the target file.
#  This uses indirect references.

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


# A multi-line awk script is invoked by   awk ' ..... '


# Begin awk script.
# ------------------------------------------------
awk "

{ total += \$${column_number} # indirect reference
}
END {
     print total
     }

     " "$filename"
# ------------------------------------------------
# End awk script.

#  Indirect variable reference avoids the hassles
#+  of referencing a shell variable within the embedded awk script.
#  Thanks, Stephane Chazelas.


exit 0
