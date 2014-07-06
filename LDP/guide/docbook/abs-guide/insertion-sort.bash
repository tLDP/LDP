#!/bin/bash
# insertion-sort.bash: Insertion sort implementation in Bash
#                      Heavy use of Bash array features:
#+                     (string) slicing, merging, etc
# URL: http://www.lugmen.org.ar/~jjo/jjotip/insertion-sort.bash.d
#+          /insertion-sort.bash.sh
#
# Author: JuanJo Ciarlante &lt;jjo@irrigacion.gov.ar&gt;
# Lightly reformatted by ABS Guide author.
# License: GPLv2
# Used in ABS Guide with author's permission (thanks!).
#
# Test with:   ./insertion-sort.bash -t
# Or:          bash insertion-sort.bash -t
# The following *doesn't* work:
#              sh insertion-sort.bash -t
#  Why not? Hint: which Bash-specific features are disabled
#+ when running a script by 'sh script.sh'?
#
: ${DEBUG:=0}  # Debug, override with:  DEBUG=1 ./scriptname . . .
# Parameter substitution -- set DEBUG to 0 if not previously set.

# Global array: "list"
typeset -a list
# Load whitespace-separated numbers from stdin.
if [ "$1" = "-t" ]; then
DEBUG=1
        read -a list &lt; &lt;( od -Ad -w24 -t u2 /dev/urandom ) # Random list.
#                    ^ ^  process substition
else
        read -a list
fi
numelem=${#list[*]}

#  Shows the list, marking the element whose index is $1
#+ by surrounding it with the two chars passed as $2.
#  Whole line prefixed with $3.
showlist()
  {
  echo "$3"${list[@]:0:$1} ${2:0:1}${list[$1]}${2:1:1} ${list[@]:$1+1};
  }

# Loop _pivot_ -- from second element to end of list.
for(( i=1; i&lt;numelem; i++ )) do
        ((DEBUG))&amp;&amp;showlist i "[]" " "
        # From current _pivot_, back to first element.
        for(( j=i; j; j-- )) do
                # Search for the 1st elem. less than current "pivot" . . .
                [[ "${list[j-1]}" -le "${list[i]}" ]] &amp;&amp; break
        done
	(( i==j )) &amp;&amp; continue ## No insertion was needed for this element.
	# . . . Move list[i] (pivot) to the left of list[j]:
        list=(${list[@]:0:j} ${list[i]} ${list[j]}\
	#         {0,j-1}        {i}       {j}
              ${list[@]:j+1:i-(j+1)} ${list[@]:i+1})
	#         {j+1,i-1}              {i+1,last}
	((DEBUG))&amp;&amp;showlist j "&lt;&gt;" "*"
done


echo
echo  "------"
echo $'Result:\n'${list[@]}

exit $?
