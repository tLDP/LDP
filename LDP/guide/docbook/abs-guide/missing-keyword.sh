#!/bin/bash
# missing-keyword.sh: What error message will this generate?

for a in 1 2 3
do
  echo "$a"
# done     # Required keyword 'done' commented out in line 7.

exit 0  

# === #

echo $?    # 2
