#!/bin/bash

PS3='Choose your favorite vegetable: ' # Sets the prompt string.

echo

select vegetable in "beans" "carrots" "potatoes" "onions" "rutabagas"
do
  echo
  echo "Your favorite veggie is $vegetable."
  echo "Yuck!"
  echo
  break  # if no 'break' here, keeps looping forever.
done

exit 0
