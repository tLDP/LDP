#!/bin/bash

y=`eval ls -l`
echo $y

y=`eval df`
echo $y
# Note that LF's not preserved

exit 0
