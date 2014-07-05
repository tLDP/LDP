#!/bin/bash
# bingo.sh
# Bingo number generator
# Reldate 20Aug12, License: Public Domain

#######################################################################
# This script generates bingo numbers.
# Hitting a key generates a new number.
# Hitting 'q' terminates the script.
# In a given run of the script, there will be no duplicate numbers.
# When the script terminates, it prints a log of the numbers generated.
#######################################################################

MIN=1       # Lowest allowable bingo number.
MAX=75      # Highest allowable bingo number.
COLS=15     # Numbers in each column (B I N G O).
SINGLE_DIGIT_MAX=9

declare -a Numbers
Prefix=(B I N G O)

initialize_Numbers ()
{  # Zero them out to start.
   # They'll be incremented if chosen.
   local index=0
   until [ "$index" -gt $MAX ]
   do
     Numbers[index]=0
     ((index++))
   done

   Numbers[0]=1   # Flag zero, so it won't be selected.
}


generate_number ()
{
   local number

   while [ 1 ]
   do
     let "number = $(expr $RANDOM % $MAX)"
     if [ ${Numbers[number]} -eq 0 ]    # Number not yet called.
     then
       let "Numbers[number]+=1"         # Flag it in the array.
       break                            # And terminate loop.
     fi   # Else if already called, loop and generate another number.
   done
   # Exercise: Rewrite this more elegantly as an until-loop.

   return $number
}


print_numbers_called ()
{   # Print out the called number log in neat columns.
    # echo ${Numbers[@]}

local pre2=0                #  Prefix a zero, so columns will align
                            #+ on single-digit numbers.

echo "Number Stats"

for (( index=1; index&lt;=MAX; index++))
do
  count=${Numbers[index]}
  let "t = $index - 1"      # Normalize, since array begins with index 0.
  let "column = $(expr $t / $COLS)"
  pre=${Prefix[column]}
# echo -n "${Prefix[column]} "

if [ $(expr $t % $COLS) -eq 0 ]
then
  echo   # Newline at end of row.
fi

  if [ "$index" -gt $SINGLE_DIGIT_MAX ]  # Check for single-digit number.
  then
    echo -n "$pre$index#$count "
  else    # Prefix a zero.
    echo -n "$pre$pre2$index#$count "
  fi

done
}



# main () {
RANDOM=$$   # Seed random number generator.

initialize_Numbers   # Zero out the number tracking array.

clear
echo "Bingo Number Caller"; echo

while [[ "$key" != "q" ]]   # Main loop.
do
  read -s -n1 -p "Hit a key for the next number [q to exit] " key
  # Usually 'q' exits, but not always.
  # Can always hit Ctl-C if q fails.
  echo

  generate_number; new_number=$?

  let "column = $(expr $new_number / $COLS)"
  echo -n "${Prefix[column]} "   # B-I-N-G-O

  echo $new_number
done

echo; echo

# Game over ...
print_numbers_called
echo; echo "[#0 = not called . . . #1 = called]"

echo

exit 0
# }


# Certainly, this script could stand some improvement.
#See also the author's Instructable:
#www.instructables.com/id/Binguino-An-Arduino-based-Bingo-Number-Generato/
