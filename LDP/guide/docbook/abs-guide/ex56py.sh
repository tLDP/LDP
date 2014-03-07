#!/bin/bash
# ex56py.sh

# Shell commands may precede the Python script.
echo "This precedes the embedded Python script within \"$0.\""
echo "==============================================================="

python -c 'print "This line prints from an embedded Python script.\n";'
# Unlike sed and perl, Python uses the "-c" option.
python -c 'k = raw_input( "Hit a key to exit to outer script. " )'

echo "==============================================================="
echo "However, the script may also contain shell and system commands."

exit 0
