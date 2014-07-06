#!/bin/bash
# ktour.sh

# author: mendel cooper
# reldate: 12 Jan 2009
# license: public domain
# (Not much sense GPLing something that's pretty much in the common
#+ domain anyhow.)

###################################################################
#             The Knight's Tour, a classic problem.               #
#             =====================================               #
#  The knight must move onto every square of the chess board,     #
#  but cannot revisit any square he has already visited.          #
#                                                                 #
#  And just why is Sir Knight unwelcome for a return visit?       #
#  Could it be that he has a habit of partying into the wee hours #
#+ of the morning?                                                #
#  Possibly he leaves pizza crusts in the bed, empty beer bottles #
#+ all over the floor, and clogs the plumbing. . . .              #
#                                                                 #
#  -------------------------------------------------------------  #
#                                                                 #
#  Usage: ktour.sh [start-square] [stupid]                        #
#                                                                 #
#  Note that start-square can be a square number                  #
#+ in the range 0 - 63 ... or                                     #
#  a square designator in conventional chess notation,            #
#  such as a1, f5, h3, etc.                                       #
#                                                                 #
#  If start-square-number not supplied,                           #
#+ then starts on a random square somewhere on the board.         #
#                                                                 #
# "stupid" as second parameter sets the stupid strategy.          #
#                                                                 #
#  Examples:                                                      #
#  ktour.sh 23          starts on square #23 (h3)                 #
#  ktour.sh g6 stupid   starts on square #46,                     #
#                       using "stupid" (non-Warnsdorff) strategy. #
###################################################################

DEBUG=      # Set this to echo debugging info to stdout.
SUCCESS=0
FAIL=99
BADMOVE=-999
FAILURE=1
LINELEN=21  # How many moves to display per line.
# ---------------------------------------- #
# Board array params
ROWS=8   # 8 x 8 board.
COLS=8
let "SQUARES = $ROWS * $COLS"
let "MAX = $SQUARES - 1"
MIN=0
# 64 squares on board, indexed from 0 to 63.

VISITED=1
UNVISITED=-1
UNVSYM="##"
# ---------------------------------------- #
# Global variables.
startpos=    # Starting position (square #, 0 - 63).
currpos=     # Current position.
movenum=     # Move number.
CRITPOS=37   # Have to patch for f5 starting position!

declare -i board
# Use a one-dimensional array to simulate a two-dimensional one.
# This can make life difficult and result in ugly kludges; see below.
declare -i moves  # Offsets from current knight position.


initialize_board ()
{
  local idx

  for idx in {0..63}
  do
    board[$idx]=$UNVISITED
  done
}



print_board ()
{
  local idx

  echo "    _____________________________________"
  for row in {7..0}               #  Reverse order of rows ...
  do                              #+ so it prints in chessboard order.
    let "rownum = $row + 1"       #  Start numbering rows at 1.
    echo -n "$rownum  |"          #  Mark board edge with border and
    for column in {0..7}          #+ "algebraic notation."
    do
      let "idx = $ROWS*$row + $column"
      if [ ${board[idx]} -eq $UNVISITED ]
      then
        echo -n "$UNVSYM   "      ##
      else                        # Mark square with move number.
        printf "%02d " "${board[idx]}"; echo -n "  "
      fi
    done
    echo -e -n "\b\b\b|"  # \b is a backspace.
    echo                  # -e enables echoing escaped chars.
  done

  echo "    -------------------------------------"
  echo "     a    b    c    d    e    f    g    h"
}



failure()
{ # Whine, then bail out.
  echo
  print_board
  echo
  echo    "   Waah!!! Ran out of squares to move to!"
  echo -n "   Knight's Tour attempt ended"
  echo    " on $(to_algebraic $currpos) [square #$currpos]"
  echo    "   after just $movenum moves!"
  echo
  exit $FAIL
}



xlat_coords ()   #  Translate x/y coordinates to board position
{                #+ (board-array element #).
  #  For user input of starting board position as x/y coords.
  #  This function not used in initial release of ktour.sh.
  #  May be used in an updated version, for compatibility with
  #+ standard implementation of the Knight's Tour in C, Python, etc.
  if [ -z "$1" -o -z "$2" ]
  then
    return $FAIL
  fi

  local xc=$1
  local yc=$2

  let "board_index = $xc * $ROWS + yc"

  if [ $board_index -lt $MIN -o $board_index -gt $MAX ]
  then
    return $FAIL    # Strayed off the board!
  else
    return $board_index
  fi
}



to_algebraic ()   #  Translate board position (board-array element #)
{                 #+ to standard algebraic notation used by chess players.
  if [ -z "$1" ]
  then
    return $FAIL
  fi

  local element_no=$1   # Numerical board position.
  local col_arr=( a b c d e f g h )
  local row_arr=( 1 2 3 4 5 6 7 8 )

  let "row_no = $element_no / $ROWS"
  let "col_no = $element_no % $ROWS"
  t1=${col_arr[col_no]}; t2=${row_arr[row_no]}
  local apos=$t1$t2   # Concatenate.
  echo $apos
}



from_algebraic ()   #  Translate standard algebraic chess notation
{                   #+ to numerical board position (board-array element #).
                    #  Or recognize numerical input &amp; return it unchanged.
  if [ -z "$1" ]
  then
    return $FAIL
  fi   # If no command-line arg, then will default to random start pos.

  local ix
  local ix_count=0
  local b_index     # Board index [0-63]
  local alpos="$1"

  arow=${alpos:0:1} # position = 0, length = 1
  acol=${alpos:1:1}

  if [[ $arow =~ [[:digit:]] ]]   #  Numerical input?
  then       #  POSIX char class
    if [[ $acol =~ [[:alpha:]] ]] # Number followed by a letter? Illegal!
      then return $FAIL
    else if [ $alpos -gt $MAX ]   # Off board?
      then return $FAIL
    else return $alpos            #  Return digit(s) unchanged . . .
      fi                          #+ if within range.
    fi
  fi

  if [[ $acol -eq $MIN || $acol -gt $ROWS ]]
  then        # Outside of range 1 - 8?
    return $FAIL
  fi

  for ix in a b c d e f g h
  do  # Convert column letter to column number.
   if [ "$arow" = "$ix" ]
   then
     break
   fi
  ((ix_count++))    # Find index count.
  done

  ((acol--))        # Decrementing converts to zero-based array.
  let "b_index = $ix_count + $acol * $ROWS"

  if [ $b_index -gt $MAX ]   # Off board?
  then
    return $FAIL
  fi
    
  return $b_index

}


generate_moves ()   #  Calculate all valid knight moves,
{                   #+ relative to current position ($1),
                    #+ and store in ${moves} array.
  local kt_hop=1    #  One square  :: short leg of knight move.
  local kt_skip=2   #  Two squares :: long leg  of knight move.
  local valmov=0    #  Valid moves.
  local row_pos; let "row_pos = $1 % $COLS"


  let "move1 = -$kt_skip + $ROWS"           # 2 sideways to-the-left,  1 up
    if [[ `expr $row_pos - $kt_skip` -lt $MIN ]]   # An ugly, ugly kludge!
    then                                           # Can't move off board.
      move1=$BADMOVE                               # Not even temporarily.
    else
      ((valmov++))
    fi
  let "move2 = -$kt_hop + $kt_skip * $ROWS" # 1 sideways to-the-left,  2 up
    if [[ `expr $row_pos - $kt_hop` -lt $MIN ]]    # Kludge continued ...
    then
      move2=$BADMOVE
    else
      ((valmov++))
    fi
  let "move3 =  $kt_hop + $kt_skip * $ROWS" # 1 sideways to-the-right, 2 up
    if [[ `expr $row_pos + $kt_hop` -ge $COLS ]]
    then
      move3=$BADMOVE
    else
      ((valmov++))
    fi
  let "move4 =  $kt_skip + $ROWS"           # 2 sideways to-the-right, 1 up
    if [[ `expr $row_pos + $kt_skip` -ge $COLS ]]
    then
      move4=$BADMOVE
    else
      ((valmov++))
    fi
  let "move5 =  $kt_skip - $ROWS"           # 2 sideways to-the-right, 1 dn
    if [[ `expr $row_pos + $kt_skip` -ge $COLS ]]
    then
      move5=$BADMOVE
    else
      ((valmov++))
    fi
  let "move6 =  $kt_hop - $kt_skip * $ROWS" # 1 sideways to-the-right, 2 dn
    if [[ `expr $row_pos + $kt_hop` -ge $COLS ]]
    then
      move6=$BADMOVE
    else
      ((valmov++))
    fi
  let "move7 = -$kt_hop - $kt_skip * $ROWS" # 1 sideways to-the-left,  2 dn
    if [[ `expr $row_pos - $kt_hop` -lt $MIN ]]
    then
      move7=$BADMOVE
    else
      ((valmov++))
    fi
  let "move8 = -$kt_skip - $ROWS"           # 2 sideways to-the-left,  1 dn
    if [[ `expr $row_pos - $kt_skip` -lt $MIN ]]
    then
      move8=$BADMOVE
    else
      ((valmov++))
    fi   # There must be a better way to do this.

  local m=( $valmov $move1 $move2 $move3 $move4 $move5 $move6 $move7 $move8 )
  # ${moves[0]} = number of valid moves.
  # ${moves[1]} ... ${moves[8]} = possible moves.
  echo "${m[*]}"    # Elements of array to stdout for capture in a var.

}



is_on_board ()  # Is position actually on the board?
{
  if [[ "$1" -lt "$MIN" || "$1" -gt "$MAX" ]]
  then
    return $FAILURE
  else
    return $SUCCESS
  fi
}



do_move ()      # Move the knight!
{
  local valid_moves=0
  local aapos
  currposl="$1"
  lmin=$ROWS
  iex=0
  squarel=
  mpm=
  mov=
  declare -a p_moves

  ########################## DECIDE-MOVE #############################
  if [ $startpos -ne $CRITPOS ]
  then   # CRITPOS = square #37
    decide_move
  else                     # Needs a special patch for startpos=37 !!!
    decide_move_patched    # Why this particular move and no other ???
  fi
  ####################################################################

  (( ++movenum ))          # Increment move count.
  let "square = $currposl + ${moves[iex]}"

  ##################    DEBUG    ###############
  if [ "$DEBUG" ]
    then debug   # Echo debugging information.
  fi
  ##############################################

  if [[ "$square" -gt $MAX || "$square" -lt $MIN ||
        ${board[square]} -ne $UNVISITED ]]
  then
    (( --movenum ))              #  Decrement move count,
    echo "RAN OUT OF SQUARES!!!" #+ since previous one was invalid.
    return $FAIL
  fi

  board[square]=$movenum
  currpos=$square       # Update current position.
  ((valid_moves++));    # moves[0]=$valid_moves
  aapos=$(to_algebraic $square)
  echo -n "$aapos "
  test $(( $Moves % $LINELEN )) -eq 0 &amp;&amp; echo
  # Print LINELEN=21 moves per line. A valid tour shows 3 complete lines.
  return $valid_moves   # Found a square to move to!
}



do_move_stupid()   #  Dingbat algorithm,
{                  #+ courtesy of script author, *not* Warnsdorff.
  local valid_moves=0
  local movloc
  local squareloc
  local aapos
  local cposloc="$1"

  for movloc in {1..8}
  do       # Move to first-found unvisited square.
    let "squareloc = $cposloc + ${moves[movloc]}"
    is_on_board $squareloc
    if [ $? -eq $SUCCESS ] &amp;&amp; [ ${board[squareloc]} -eq $UNVISITED ]
    then   # Add conditions to above if-test to improve algorithm.
      (( ++movenum ))
      board[squareloc]=$movenum
      currpos=$squareloc     # Update current position.
      ((valid_moves++));     # moves[0]=$valid_moves
      aapos=$(to_algebraic $squareloc)
      echo -n "$aapos "
      test $(( $Moves % $LINELEN )) -eq 0 &amp;&amp; echo   # Print 21 moves/line.
      return $valid_moves    # Found a square to move to!
    fi
  done

  return $FAIL
  #  If no square found in all 8 loop iterations,
  #+ then Knight's Tour attempt ends in failure.

  #  Dingbat algorithm will typically fail after about 30 - 40 moves,
  #+ but executes _much_ faster than Warnsdorff's in do_move() function.
}



decide_move ()         #  Which move will we make?
{                      #  But, fails on startpos=37 !!!
  for mov in {1..8}
  do
    let "squarel = $currposl + ${moves[mov]}"
    is_on_board $squarel
    if [[ $? -eq $SUCCESS &amp;&amp; ${board[squarel]} -eq $UNVISITED ]]
    then   #  Find accessible square with least possible future moves.
           #  This is Warnsdorff's algorithm.
           #  What happens is that the knight wanders toward the outer edge
           #+ of the board, then pretty much spirals inward.
           #  Given two or more possible moves with same value of
           #+ least-possible-future-moves, this implementation chooses
           #+ the _first_ of those moves.
           #  This means that there is not necessarily a unique solution
           #+ for any given starting position.

      possible_moves $squarel
      mpm=$?
      p_moves[mov]=$mpm
      
      if [ $mpm -lt $lmin ]  # If less than previous minimum ...
      then #     ^^
        lmin=$mpm            # Update minimum.
        iex=$mov             # Save index.
      fi

    fi
  done
}



decide_move_patched ()         #  Decide which move to make,
{  #        ^^^^^^^            #+ but only if startpos=37 !!!
  for mov in {1..8}
  do
    let "squarel = $currposl + ${moves[mov]}"
    is_on_board $squarel
    if [[ $? -eq $SUCCESS &amp;&amp; ${board[squarel]} -eq $UNVISITED ]]
    then
      possible_moves $squarel
      mpm=$?
      p_moves[mov]=$mpm
      
      if [ $mpm -le $lmin ]  # If less-than-or equal to prev. minimum!
      then #     ^^
        lmin=$mpm
        iex=$mov
      fi

    fi
  done                       # There has to be a better way to do this.
}



possible_moves ()            #  Calculate number of possible moves,
{                            #+ given the current position.

  if [ -z "$1" ]
  then
    return $FAIL
  fi

  local curr_pos=$1
  local valid_movl=0
  local icx=0
  local movl
  local sq
  declare -a movesloc

  movesloc=( $(generate_moves $curr_pos) )

  for movl in {1..8}
  do
    let "sq = $curr_pos + ${movesloc[movl]}"
    is_on_board $sq
    if [ $? -eq $SUCCESS ] &amp;&amp; [ ${board[sq]} -eq $UNVISITED ]
    then
      ((valid_movl++));
    fi
  done

  return $valid_movl         # Found a square to move to!
}


strategy ()
{
  echo

  if [ -n "$STUPID" ]
  then
    for Moves in {1..63}
    do
      cposl=$1
      moves=( $(generate_moves $currpos) )
      do_move_stupid "$currpos"
      if [ $? -eq $FAIL ]
      then
        failure
      fi
      done
  fi

  #  Don't need an "else" clause here,
  #+ because Stupid Strategy will always fail and exit!
  for Moves in {1..63}
  do
    cposl=$1
    moves=( $(generate_moves $currpos) )
    do_move "$currpos"
    if [ $? -eq $FAIL ]
    then
      failure
    fi

  done
        #  Could have condensed above two do-loops into a single one,
  echo  #+ but this would have slowed execution.

  print_board
  echo
  echo "Knight's Tour ends on $(to_algebraic $currpos) [square #$currpos]."
  return $SUCCESS
}

debug ()
{       # Enable this by setting DEBUG=1 near beginning of script.
  local n

  echo "================================="
  echo "  At move number  $movenum:"
  echo " *** possible moves = $mpm ***"
# echo "### square = $square ###"
  echo "lmin = $lmin"
  echo "${moves[@]}"

  for n in {1..8}
  do
    echo -n "($n):${p_moves[n]} "
  done

  echo
  echo "iex = $iex :: moves[iex] = ${moves[iex]}"
  echo "square = $square"
  echo "================================="
  echo
} # Gives pretty complete status after ea. move.



# =============================================================== #
# int main () {
from_algebraic "$1"
startpos=$?
if [ "$startpos" -eq "$FAIL" ]          # Okay even if no $1.
then   #         ^^^^^^^^^^^              Okay even if input -lt 0.
  echo "No starting square specified (or illegal input)."
  let "startpos = $RANDOM % $SQUARES"   # 0 - 63 permissable range.
fi


if [ "$2" = "stupid" ]
then
  STUPID=1
  echo -n "     ### Stupid Strategy ###"
else
  STUPID=''
  echo -n "  *** Warnsdorff's Algorithm ***"
fi


initialize_board

movenum=0
board[startpos]=$movenum   # Mark each board square with move number.
currpos=$startpos
algpos=$(to_algebraic $startpos)

echo; echo "Starting from $algpos [square #$startpos] ..."; echo
echo -n "Moves:"

strategy "$currpos"

echo

exit 0   # return 0;

# }      # End of main() pseudo-function.
# =============================================================== #


# Exercises:
# ---------
#
# 1) Extend this example to a 10 x 10 board or larger.
# 2) Improve the "stupid strategy" by modifying the
#    do_move_stupid function.
#    Hint: Prevent straying into corner squares in early moves
#          (the exact opposite of Warnsdorff's algorithm!).
# 3) This script could stand considerable improvement and
#    streamlining, especially in the poorly-written
#    generate_moves() function
#    and in the DECIDE-MOVE patch in the do_move() function.
#    Must figure out why standard algorithm fails for startpos=37 ...
#+   but _not_ on any other, including symmetrical startpos=26.
#    Possibly, when calculating possible moves, counts the move back
#+   to the originating square. If so, it might be a relatively easy fix.
