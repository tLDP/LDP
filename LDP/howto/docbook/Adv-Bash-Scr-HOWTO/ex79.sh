#!/bin/bash2
# Must specify version 2 of bash, else might not work.

# Cards:
# deals four random hands from a deck of cards.

UNPICKED=0
PICKED=1

DUPE_CARD=99

LOWER_LIMIT=0
UPPER_LIMIT=51
CARDS_IN_SUITE=13
CARDS=52

declare -a Deck
declare -a Suites
declare -a Cards
# It would have been easier and more intuitive
# with a single, 3-dimensional array. Maybe 
# a future version of bash will support
# multidimensional arrays.


initialize_Deck ()
{
i=$LOWER_LIMIT
until [ $i -gt $UPPER_LIMIT ]
do
  Deck[i]=$UNPICKED
  let "i += 1"
done
# Set each card of "Deck" as unpicked.
echo
}

initialize_Suites ()
{
Suites[0]=C #Clubs
Suites[1]=D #Diamonds
Suites[2]=H #Hearts
Suites[3]=S #Spades
}

initialize_Cards ()
{
Cards=(2 3 4 5 6 7 8 9 10 J Q K A)
# Alternate method of initializing array.
}

pick_a_card ()
{
card_number=$RANDOM
let "card_number %= $CARDS"
if [ ${Deck[card_number]} -eq $UNPICKED ]
then
  Deck[card_number]=$PICKED
  return $card_number
else  
  return $DUPE_CARD
fi
}

parse_card ()
{
number=$1
let "suite_number = number / CARDS_IN_SUITE"
suite=${Suites[suite_number]}
echo -n "$suite-"
let "card_no = number % CARDS_IN_SUITE"
Card=${Cards[card_no]}
printf %-4s $Card
# Print cards in neat columns.
}

seed_random ()
{
# Seed random number generator.
seed=`eval date +%s`
let "seed %= 32766"
RANDOM=$seed
}

deal_cards ()
{
echo

cards_picked=0
while [ $cards_picked -le $UPPER_LIMIT ]
do
  pick_a_card
  t=$?

  if [ $t -ne $DUPE_CARD ]
  then
    parse_card $t

    u=$cards_picked+1
    # Change back to 1-based indexing (temporarily).
    let "u %= $CARDS_IN_SUITE"
    if [ $u -eq 0 ]
    then
     echo
     echo
    fi
    # Separate hands.

    let "cards_picked += 1"
  fi  
done  

echo

return 0
}


# Structured programming:
# entire program logic modularized in functions.

#================
seed_random
initialize_Deck
initialize_Suites
initialize_Cards
deal_cards

exit 0
#================



# Exercise 1:
# Add comments to thoroughly document this script.

# Exercise 2:
# Revise the script to print out each hand sorted in suites.
# You may add other bells and whistles if you like.

# Exercise 3:
# Simplify and streamline the logic of the script.
