#!/bin/bash
# rot13.sh: Classic rot13 algorithm,
#           encryption that might fool a 3-year old.

# Usage: ./rot13.sh filename
# or     ./rot13.sh &lt;filename
# or     ./rot13.sh and supply keyboard input (stdin)

cat "$@" | tr 'a-zA-Z' 'n-za-mN-ZA-M'   # "a" goes to "n", "b" to "o", etc.
#  The 'cat "$@"' construction
#+ permits getting input either from stdin or from files.

exit 0
