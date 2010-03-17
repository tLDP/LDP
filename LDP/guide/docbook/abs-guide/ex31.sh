#!/bin/bash

PS3='Choose your favorite vegetable: ' # Sets the prompt string.
                                       # Otherwise it defaults to #? .

echo

select vegetable in "beans" "carrots" "potatoes" "onions" "rutabagas"
do
  echo
  echo "Your favorite veggie is $vegetable."
  echo "Yuck!"
  echo
  break  # What happens if there is no 'break' here?
done

exit

# Exercise:
# --------
#  Fix this script to accept user input not specified in
#+ the "select" statement.
#  For example, if the user inputs "peas,"
#+ the script would respond "Sorry. That is not on the menu."
