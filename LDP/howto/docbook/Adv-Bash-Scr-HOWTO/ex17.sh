#!/bin/bash

echo

echo The name of this script is $0
# Adds ./ for current directory
echo The name of this script is `basename $0`
# Strip out path name info (see 'basename')

echo

if [ $1 ]
then
 echo "Parameter #1 is $1"
 # Need quotes to escape #
fi 

if [ $2 ]
then
 echo "Parameter #2 is $2"
fi 

if [ $3 ]
then
 echo "Parameter #3 is $3"
fi 

echo

exit 0
