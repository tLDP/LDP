#!/bin/bash
# broken-link.sh
# Written by Lee bigelow &lt;ligelowbee@yahoo.com&gt;
# Used in ABS Guide with permission.

#  A pure shell script to find dead symlinks and output them quoted
#+ so they can be fed to xargs and dealt with :)
#+ eg. sh broken-link.sh /somedir /someotherdir|xargs rm
#
#  This, however, is a better method:
#
#  find "somedir" -type l -print0|\
#  xargs -r0 file|\
#  grep "broken symbolic"|
#  sed -e 's/^\|: *broken symbolic.*$/"/g'
#
#+ but that wouldn't be pure Bash, now would it.
#  Caution: beware the /proc file system and any circular links!
################################################################


#  If no args are passed to the script set directories-to-search 
#+ to current directory.  Otherwise set the directories-to-search 
#+ to the args passed.
######################

[ $# -eq 0 ] &amp;&amp; directorys=`pwd` || directorys=$@


#  Setup the function linkchk to check the directory it is passed 
#+ for files that are links and don't exist, then print them quoted.
#  If one of the elements in the directory is a subdirectory then 
#+ send that subdirectory to the linkcheck function.
##########

linkchk () {
    for element in $1/*; do
      [ -h "$element" -a ! -e "$element" ] &amp;&amp; echo \"$element\"
      [ -d "$element" ] &amp;&amp; linkchk $element
    # Of course, '-h' tests for symbolic link, '-d' for directory.
    done
}

#  Send each arg that was passed to the script to the linkchk() function
#+ if it is a valid directoy.  If not, then print the error message
#+ and usage info.
##################
for directory in $directorys; do
    if [ -d $directory ]
	then linkchk $directory
	else 
	    echo "$directory is not a directory"
	    echo "Usage: $0 dir1 dir2 ..."
    fi
done

exit $?
