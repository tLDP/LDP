#!/bin/bash

func2 () {
   if [ -z "$1" ]
   # Checks if parameter #1 is zero length.
   then
     echo "-Parameter #1 is zero length.-"  # Also if no parameter is passed.
   else
     echo "-Param #1 is \"$1\".-"
   fi

   if [ "$2" ]
   then
     echo "-Parameter #2 is \"$2\".-"
   fi

   return 0
}

echo
   
echo "Nothing passed."   
func2                          # Called with no params
echo


echo "Zero-length parameter passed."
func2 ""                       # Called with zero-length param
echo

echo "Null parameter passed."
func2 "$uninitialized_param"   # Called with uninitialized param
echo

echo "One parameter passed."   
func2 first           # Called with one param
echo

echo "Two parameter passed."   
func2 first second    # Called with two params
echo

echo "\"\" \"second\" passed."
func2 "" second       # Called with zero-length first parameter
echo                  # and ASCII string as a second one.

exit 0
