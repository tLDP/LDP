#!/bin/bash

# 'getopts' processes command line args to script.

# Usage: scriptname -options
# Note: dash (-) necessary

# Try invoking this script with
# 'scriptname -mn'
# 'scriptname -oq qOption'
# (qOption can be some arbitrary string.)

OPTERROR=33

if [ -z $1 ]
# Exit and complain if no argument(s) given.
then
  echo "Usage: `basename $0` options (-mnopqrs)"
  exit $OPTERROR
fi  

while getopts ":mnopq:rs" Option
do
  case $Option in
    m     ) echo "Scenario #1: option -m-";;
    n | o ) echo "Scenario #2: option -$Option-";;
    p     ) echo "Scenario #3: option -p-";;
    q     ) echo "Scenario #4: option -q-, with argument \"$OPTARG\"";;
    # Note that option 'q' must have an additional argument,
    # otherwise nothing happens.
    r | s ) echo "Scenario #5: option -$Option-"'';;
    *     ) echo "Unimplemented option chosen.";;
  esac
done

shift $(($OPTIND - 1))
# Decrements the argument pointer
# so it points to next argument.

exit 0
