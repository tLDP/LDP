#!/bin/bash

# Example "ex72.sh" modified to use encrypted password.

E_BADARGS=65

if [ -z "$1" ]
then
  echo "Usage: `basename $0` filename"
  exit $E_BADARGS
fi  

Username=bozo           # Change to suit.

Filename=`basename $1`  # Strips pathname out of file name

Server="XXX"
Directory="YYY"         # Change above to actual server name & directory.


password=`cruft &lt;pword`
# "pword" is the file containing encrypted password.
# Uses the author's own "cruft" file encryption package,
# based on the classic "onetime pad" algorithm,
# and obtainable from:
# Primary-site:   ftp://metalab.unc.edu /pub/Linux/utils/file
#                 cruft-0.2.tar.gz [16k]


ftp -n $Server &lt;&lt;End-Of-Session
user $Username $Password
binary
bell
cd $Directory
put $Filename
bye
End-Of-Session
# -n option to "ftp" disables auto-logon.
# "bell" rings 'bell' after each file transfer.

exit 0
