#! /bin/bash
#
# Changes every filename in working directory to all lowercase.
#
# Inspired by a script of john dubois,
# which was translated into into bash by Chet Ramey,
# and considerably simplified by Mendel Cooper,
# author of this HOWTO.


for filename in *  #Traverse all files in directory.
do
   fname=`basename $filename`
   n=`echo $fname | tr A-Z a-z`  #Change name to lowercase.
   if [ $fname != $n ]  # Rename only files not already lowercase.
   then
     mv $fname $n
   fi  
done   

exit 0
