#!/bin/bash

# Example 3-71 modified to use encrypted password.

if [ -z "$1" ]
then
  echo "Usage: `basename $0` filename"
  exit 65
fi  

Username=bozo
# Change to suit.

Filename=`basename $1`
# Strips pathname out of file name

Server="XXX"
Directory="YYY"
# Change above to actual server name & directory.


password=`cruft &lt;pword`
# "pword" is the file containing encrypted password.
# Uses the author's own "cruft" file encryption package,
# based on the classic "onetime pad" algorithm,
# and obtainable from:
# Primary-site:   ftp://metalab.unc.edu /pub/Linux/utils/file
#                 cruft-0.2.tar.gz [16k]


ftp -n $Server &lt;&lt;End-Of-Session
# -n option disables auto-logon

user $Username $Password
binary
bell
# Ring 'bell' after each file transfer
cd $Directory
put $Filename
bye
End-Of-Session

exit 0
