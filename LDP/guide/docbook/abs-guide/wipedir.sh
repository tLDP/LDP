#!/bin/bash

E_WRONG_DIRECTORY=73

clear # Clear screen.

TargetDirectory=/home/bozo/projects/GreatAmericanNovel

cd $TargetDirectory
echo "Deleting stale files in $TargetDirectory."

if [ "$PWD" != "$TargetDirectory" ]
then    # Keep from wiping out wrong directory by accident.
  echo "Wrong directory!"
  echo "In $PWD, rather than $TargetDirectory!"
  echo "Bailing out!"
  exit $E_WRONG_DIRECTORY
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
