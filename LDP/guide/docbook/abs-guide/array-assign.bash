#! /bin/bash
# array-assign.bash

#  Array operations are Bash specific,
#+ hence the ".bash" in the script name.

# Copyright (c) Michael S. Zick, 2003, All rights reserved.
# License: Unrestricted reuse in any form, for any purpose.
# Version: $ID$
#
# Clarification and additional comments by William Park.

#  Based on an example provided by Stephane Chazelas
#+ which appeared in the book: Advanced Bash Scripting Guide.

# Output format of the 'times' command:
# User CPU &lt;space&gt; System CPU
# User CPU of dead children &lt;space&gt; System CPU of dead children

#  Bash has two versions of assigning all elements of an array
#+ to a new array variable.
#  Both drop 'null reference' elements
#+ in Bash versions 2.04, 2.05a and 2.05b.
#  An additional array assignment that maintains the relationship of
#+ [subscript]=value for arrays may be added to newer versions.

#  Constructs a large array using an internal command,
#+ but anything creating an array of several thousand elements
#+ will do just fine.

declare -a bigOne=( /dev/* )
echo
echo 'Conditions: Unquoted, default IFS, All-Elements-Of'
echo "Number of elements in array is ${#bigOne[@]}"

# set -vx



echo
echo '- - testing: =( ${array[@]} ) - -'
times
declare -a bigTwo=( ${bigOne[@]} )
#                 ^              ^
times

echo
echo '- - testing: =${array[@]} - -'
times
declare -a bigThree=${bigOne[@]}
# No parentheses this time.
times

#  Comparing the numbers shows that the second form, pointed out
#+ by Stephane Chazelas, is from three to four times faster.
#
#  William Park explains:
#+ Second method is assigning bigOne[] as single string, whereas first
#+  method is assigning bigOne[] element by element.  So, in essence, you
#   So, in essence, you have:
#                   bigTwo=( [0]="... ... ..." )
#                   bigThree=( [0]="..." [1]="..." [2]="..." ... )


#  I will continue to use the first form in my example descriptions
#+ because I think it is a better illustration of what is happening.

#  The reusable portions of my examples will actual contain
#+ the second form where appropriate because of the speedup.

# MSZ: Sorry about that earlier oversight folks.


#  Note:
#  ----
#  The "declare -a" statements in lines 31 and 43
#+ are not strictly necessary, since it is implicit
#+ in the  Array=( ... )  assignment form.
#  However, eliminating these declarations slows down
#+ the execution of the following sections of the script.
#  Try it, and see what happens.

exit 0
