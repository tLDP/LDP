#!/bin/bash
# t-out.sh (per a suggestion by "syngin seven)

TIMELIMIT=4        # 4 seconds

read -t $TIMELIMIT variable <&1

echo

if [ -z "$variable" ]
then
  echo "Timed out, variable still unset."
else  
  echo "variable = $variable"
fi  

exit 0
