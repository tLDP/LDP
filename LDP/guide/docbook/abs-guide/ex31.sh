#!/bin/bash

PS3='Choose your favorite vegetable: ' # Sets the prompt string.

echo

select vegetable in "beans" "carrots" "potatoes" "onions" "rutabagas"
do
  echo
  echo "Your favorite veggie is $vegetable."
  echo "Yuck!"
  echo
  break  # What happens if there is no 'break' here?
done

exit 0
