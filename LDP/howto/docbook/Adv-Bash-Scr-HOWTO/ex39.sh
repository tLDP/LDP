#!/bin/bash

if [ -z $1 ]
then
  echo "Usage: `basename $0` find-string"
  exit 1
fi

echo "Updating 'locate' database..."
echo "This may take a while."
updatedb /usr &
# Must be run as root.

wait
# Don't run the rest of the script
# until 'updatedb' finished.
# In this case, you want the the database updated
# before looking up the file name.

locate $1


exit 0
