#! /bin/bash
# The Towers Of Hanoi
# Original script (hanoi.bash) copyright (C) 2000 Amit Singh.
# All Rights Reserved.
# http://hanoi.kernelthread.com

#  hanoi2.bash
#  Version 2.00: modded for ASCII-graphic display.
#  Version 2.01: fixed no command-line param bug.
#  Uses code contributed by Antonio Macchi,
#+ with heavy editing by ABS Guide author.
#  This variant falls under the original copyright, see above.
#  Used in ABS Guide with Amit Singh's permission (thanks!).


###   Variables &amp;&amp; sanity check   ###

E_NOPARAM=86
E_BADPARAM=87            # Illegal no. of disks passed to script.
E_NOEXIT=88

DISKS=${1:-$E_NOPARAM}   # Must specify how many disks.
Moves=0

MWIDTH=7
MARGIN=2
# Arbitrary "magic" constants; work okay for relatively small # of disks.
# BASEWIDTH=51   # Original code.
let "basewidth = $MWIDTH * $DISKS + $MARGIN"       # "Base" beneath rods.
# Above "algorithm" could likely stand improvement.

###   Display variables   ###
let "disks1 = $DISKS - 1"
let "spaces1 = $DISKS" 
let "spaces2 = 2 * $DISKS" 

let "lastmove_t = $DISKS - 1"                      # Final move?


declare -a Rod1 Rod2 Rod3

###   #########################   ###


function repeat  {  # $1=char $2=number of repetitions
  local n           # Repeat-print a character.
  
  for (( n=0; n&lt;$2; n++ )); do
    echo -n "$1"
  done
}

function FromRod  {
  local rod summit weight sequence

  while true; do
    rod=$1
    test ${rod/[^123]/} || continue

    sequence=$(echo $(seq 0 $disks1 | tac))
    for summit in $sequence; do
      eval weight=\${Rod${rod}[$summit]}
      test $weight -ne 0 &amp;&amp;
           { echo "$rod $summit $weight"; return; }
    done
  done
}


function ToRod  { # $1=previous (FromRod) weight
  local rod firstfree weight sequence
  
  while true; do
    rod=$2
    test ${rod/[^123]} || continue

    sequence=$(echo $(seq 0 $disks1 | tac))
    for firstfree in $sequence; do
      eval weight=\${Rod${rod}[$firstfree]}
      test $weight -gt 0 &amp;&amp; { (( firstfree++ )); break; }
    done
    test $weight -gt $1 -o $firstfree = 0 &amp;&amp;
         { echo "$rod $firstfree"; return; }
  done
}


function PrintRods  {
  local disk rod empty fill sp sequence


  repeat " " $spaces1
  echo -n "|"
  repeat " " $spaces2
  echo -n "|"
  repeat " " $spaces2
  echo "|"

  sequence=$(echo $(seq 0 $disks1 | tac))
  for disk in $sequence; do
    for rod in {1..3}; do
      eval empty=$(( $DISKS - (Rod${rod}[$disk] / 2) ))
      eval fill=\${Rod${rod}[$disk]}
      repeat " " $empty
      test $fill -gt 0 &amp;&amp; repeat "*" $fill || echo -n "|"
      repeat " " $empty
    done
    echo
  done
  repeat "=" $basewidth   # Print "base" beneath rods.
  echo
}


display ()
{
  echo
  PrintRods

  # Get rod-number, summit and weight
  first=( `FromRod $1` )
  eval Rod${first[0]}[${first[1]}]=0

  # Get rod-number and first-free position
  second=( `ToRod ${first[2]} $2` )
  eval Rod${second[0]}[${second[1]}]=${first[2]}


echo; echo; echo
if [ "${Rod3[lastmove_t]}" = 1 ]
then   # Last move? If yes, then display final position.
    echo "+  Final Position: $Moves moves"; echo
    PrintRods
  fi
}


# From here down, almost the same as original (hanoi.bash) script.

dohanoi() {   # Recursive function.
    case $1 in
    0)
        ;;
    *)
        dohanoi "$(($1-1))" $2 $4 $3
	if [ "$Moves" -ne 0 ]
        then
	  echo "+  Position after move $Moves"
        fi
        ((Moves++))
        echo -n "   Next move will be:  "
        echo $2 "-->" $3
          display $2 $3
        dohanoi "$(($1-1))" $4 $3 $2
        ;;
    esac
}


setup_arrays ()
{
  local dim n elem

  let "dim1 = $1 - 1"
  elem=$dim1

  for n in $(seq 0 $dim1)
  do
   let "Rod1[$elem] = 2 * $n + 1"
   Rod2[$n]=0
   Rod3[$n]=0
   ((elem--))
  done
}


###   Main   ###

setup_arrays $DISKS
echo; echo "+  Start Position"

case $# in
    1) case $(($1>0)) in     # Must have at least one disk.
       1)
           disks=$1
           dohanoi $1 1 3 2
#          Total moves = 2^n - 1, where n = number of disks.
	   echo
           exit 0;
           ;;
       *)
           echo "$0: Illegal value for number of disks";
           exit $E_BADPARAM;
           ;;
       esac
    ;;
    *)
       clear
       echo "usage: $0 N"
       echo "       Where \"N\" is the number of disks."
       exit $E_NOPARAM;
       ;;
esac

exit $E_NOEXIT   # Shouldn't exit here.

# Note:
# Redirect script output to a file, otherwise it scrolls off display.
