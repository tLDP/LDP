#!/bin/bash

# upload
# upload file pair (filename.lsm, filename.tar.gz)
# to incoming directory at Sunsite


if [ -z "$1" ]
then
  echo "Usage: `basename $0` filename"
  exit 65
fi  


Filename=`basename $1`
# Strips pathname out of file name

Server="metalab.unc.edu"
Directory="/incoming/Linux"
# These need not be hard-coded into script,
# may instead be changed to command line argument.

Password="your.e-mail.address"
# Change above to suit.

ftp -n $Server &lt;&lt;End-Of-Session
# -n option disables auto-logon

user anonymous "$Password"
binary
bell
# Ring 'bell' after each file transfer
cd $Directory
put "$Filename.lsm"
put "$Filename.tar.gz"
bye
End-Of-Session

exit 0
