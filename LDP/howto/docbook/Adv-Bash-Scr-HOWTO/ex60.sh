#!/bin/bash

func2 () {
   if [ -z $1 ]
   # Checks if any params.
   then
     echo "No parameters passed to function."
     return 0
   else
     echo "Param #1 is $1."
   fi

   if [ $2 ]
   then
     echo "Parameter #2 is $2."
   fi
}
   
func2
# Called with no params
echo

func2 first
# Called with one param
echo

func2 first second
# Called with two params
echo

exit 0
