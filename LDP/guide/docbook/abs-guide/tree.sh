#!/bin/sh
#         @(#) tree      1.1  30/11/95       by Jordi Sanfeliu
#                                         email: mikaku@fiwix.org
#
#         Initial version:  1.0  30/11/95
#         Next version   :  1.1  24/02/97   Now, with symbolic links
#         Patch by       :  Ian Kjos, to support unsearchable dirs
#                           email: beth13@mail.utexas.edu
#
#         Tree is a tool for view the directory tree (obvious :-) )
#

# ==> 'Tree' script used here with the permission of its author, Jordi Sanfeliu.
# ==> Comments added by the author of this document.
# ==> Argument quoting added.


search () {
   for dir in `echo *`
   # ==> `echo *` lists all the files in current working directory, without line breaks.
   # ==> Similar effect to     for dir in *
   # ==> but "dir in `echo *`" will not handle filenames with blanks.
   do
      if [ -d "$dir" ] ; then   # ==> If it is a directory (-d)...
         zz=0                   # ==> Temp variable, keeping track of directory level.
         while [ $zz != $deep ]    # Keep track of inner nested loop.
         do
            echo -n "|   "    # ==> Display vertical connector symbol,
                              # ==> with 2 spaces & no line feed in order to indent.
            zz=`expr $zz + 1` # ==> Increment zz.
         done
         if [ -L "$dir" ] ; then   # ==> If directory is a symbolic link...
            echo "+---$dir" `ls -l $dir | sed 's/^.*'$dir' //'`
	    # ==> Display horiz. connector and list directory name, but...
	    # ==> delete date/time part of long listing.
         else
            echo "+---$dir"      # ==> Display horizontal connector symbol...
                                 # ==> and print directory name.
            if cd "$dir" ; then  # ==> If can move to subdirectory...
               deep=`expr $deep + 1`   # ==> Increment depth.
               search     # with recursivity ;-)
                          # ==> Function calls itself.
               numdirs=`expr $numdirs + 1`   # ==> Increment directory count.
            fi
         fi
      fi
   done
   cd ..   # ==> Up one directory level.
   if [ "$deep" ] ; then  # ==> If depth = 0 (returns TRUE)...
      swfi=1              # ==> set flag showing that search is done.
   fi
   deep=`expr $deep - 1`  # ==> Decrement depth.
}

# - Main -
if [ $# = 0 ] ; then
   cd `pwd`    # ==> No args to script, then use current working directory.
else
   cd $1       # ==> Otherwise, move to indicated directory.
fi
echo "Initial directory = `pwd`"
swfi=0      # ==> Search finished flag.
deep=0      # ==> Depth of listing.
numdirs=0
zz=0

while [ "$swfi" != 1 ]   # While flag not set...
do
   search   # ==> Call function after initializing variables.
done
echo "Total directories = $numdirs"

exit 0
# ==> Challenge: try to figure out exactly how this script works.
