#!/bin/bash
# de-rpm.sh: Unpack an 'rpm' archive

E_NO_ARGS=65
TEMPFILE=$$.cpio                         # Tempfile with "unique" name.
                                         # $$ is process ID of script.

if [ -z "$1" ] 
then
  echo "Usage: `basename $0` filename"
exit $E_NO_ARGS
fi


rpm2cpio < $1 > $TEMPFILE                # Converts rpm archive into cpio archive.
cpio --make-directories -F $TEMPFILE -i  # Unpacks cpio archive.
rm -f $TEMPFILE                          # Deletes cpio archive.

exit 0
