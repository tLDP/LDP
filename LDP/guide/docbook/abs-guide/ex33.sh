#!/bin/bash

# 'getopts' processes command line arguments to script.
# The arguments are parsed as "options" (flags) and associated arguments.

# Try invoking this script with
# 'scriptname -mn'
# 'scriptname -oq qOption' (qOption can be some arbitrary string.)
# 'scriptname -qXXX -r'
#
# 'scriptname -qr'    - Unexpected result, takes "r" as the argument to option "q"
# 'scriptname -q -r'  - Unexpected result, same as above
#  If an option expects an argument ("flag:"), then it will grab
#  whatever is next on the command line.

NO_ARGS=0 
OPTERROR=65

if [ $# -eq "$NO_ARGS" ]  # Script invoked with no command-line args?
then
  echo "Usage: `basename $0` options (-mnopqrs)"
  exit $OPTERROR          # Exit and explain usage, if no argument(s) given.
fi  
# Usage: scriptname -options
# Note: dash (-) necessary


while getopts ":mnopq:rs" Option
do
  case $Option in
    m     ) echo "Scenario #1: option -m-";;
    n | o ) echo "Scenario #2: option -$Option-";;
    p     ) echo "Scenario #3: option -p-";;
    q     ) echo "Scenario #4: option -q-, with argument \"$OPTARG\"";;
    # Note that option 'q' must have an associated argument,
    # otherwise it falls through to the default.
    r | s ) echo "Scenario #5: option -$Option-"'';;
    *     ) echo "Unimplemented option chosen.";;   # DEFAULT
  esac
done

shift $(($OPTIND - 1))
# Decrements the argument pointer so it points to next argument.

exit 0
