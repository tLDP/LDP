#!/bin/bash
# rot13a.sh: Same as "rot13.sh" script, but writes output to "secure" file.

# Usage: ./rot13a.sh filename
# or     ./rot13a.sh &lt;filename
# or     ./rot13a.sh and supply keyboard input (stdin)

umask 177               #  File creation mask.
                        #  Files created by this script
                        #+ will have 600 permissions.

OUTFILE=decrypted.txt   #  Results output to file "decrypted.txt"
                        #+ which can only be read/written
                        #  by invoker of script (or root).

cat "$@" | tr 'a-zA-Z' 'n-za-mN-ZA-M' > $OUTFILE 
#    ^^ Input from stdin or a file.   ^^^^^^^^^^ Output redirected to file. 

exit 0
