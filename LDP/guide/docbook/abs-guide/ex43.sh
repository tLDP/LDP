#!/bin/bash

y=`eval ls -l`   # Similar to y=`ls -l`
echo $y          # but linefeeds removed.

y=`eval df`      # Similar to y=`df`
echo $y          # but linefeeds removed.

# Note that LF's not preserved,
# and this may make it easier to parse output.

exit 0
