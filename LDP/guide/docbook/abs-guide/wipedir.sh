#!/bin/bash

WRONG_DIRECTORY=33

clear # Clear screen.

TargetDirectory=/home/bozo/projects/GreatAmericanNovel

cd $TargetDirectory
echo "Deleting stale files in $TargetDirectory."

if [ "$PWD" != "$TargetDirectory" ]  # Keep from wiping out wrong directory by accident.
then
  echo "Wrong directory!"
  echo "In $PWD, rather than $TargetDirectory!"
  echo "Bailing out!"
  exit $WRONG_DIRECTORY
fi  

rm -rf *
rm .[A-Za-z0-9]*    # Delete dotfiles.
# rm -f .[^.]* ..?*   to remove filenames beginning with multiple dots.
# (shopt -s dotglob; rm -f *)   will also work.
# Thanks, S.C. for pointing this out.

# Filenames may contain all characters in the 0 - 255 range, except "/".
# Deleting files beginning with weird characters is left as an exercise.


# Various other operations here, as necessary.

echo
echo "Done."
echo "Old files deleted in $TargetDirectory."
echo


exit 0
