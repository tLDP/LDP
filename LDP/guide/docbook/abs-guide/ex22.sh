#!/bin/bash
# List the planets.

for planet in Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune Pluto
do
  echo $planet
done

echo

for planet in "Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune Pluto"
# Entire 'list' enclosed in quotes creates a single variable.
do
  echo $planet
done

exit 0
