#! /bin/sh
# letter-count2.sh: Counting letter occurrences in a text file.
#
# Script by nyal [nyal@voila.fr].
# Used in ABS Guide with permission.
# Recommented and reformatted by ABS Guide author.
# Version 1.1: Modified to work with gawk 3.1.3.
#              (Will still work with earlier versions.)


INIT_TAB_AWK=""
# Parameter to initialize awk script.
count_case=0
FILE_PARSE=$1

E_PARAMERR=85

usage()
{
    echo "Usage: letter-count.sh file letters" 2>&amp;1
    # For example:   ./letter-count2.sh filename.txt a b c
    exit $E_PARAMERR  # Too few arguments passed to script.
}

if [ ! -f "$1" ] ; then
    echo "$1: No such file." 2>&amp;1
    usage                 # Print usage message and exit.
fi 

if [ -z "$2" ] ; then
    echo "$2: No letters specified." 2>&amp;1
    usage
fi 

shift                      # Letters specified.
for letter in `echo $@`    # For each one . . .
  do
  INIT_TAB_AWK="$INIT_TAB_AWK tab_search[${count_case}] = \
  \"$letter\"; final_tab[${count_case}] = 0; " 
  # Pass as parameter to awk script below.
  count_case=`expr $count_case + 1`
done

# DEBUG:
# echo $INIT_TAB_AWK;

cat $FILE_PARSE |
# Pipe the target file to the following awk script.

# ---------------------------------------------------------------------
# Earlier version of script:
# awk -v tab_search=0 -v final_tab=0 -v tab=0 -v \
# nb_letter=0 -v chara=0 -v chara2=0 \

awk \
"BEGIN { $INIT_TAB_AWK } \
{ split(\$0, tab, \"\"); \
for (chara in tab) \
{ for (chara2 in tab_search) \
{ if (tab_search[chara2] == tab[chara]) { final_tab[chara2]++ } } } } \
END { for (chara in final_tab) \
{ print tab_search[chara] \" => \" final_tab[chara] } }"
# ---------------------------------------------------------------------
#  Nothing all that complicated, just . . .
#+ for-loops, if-tests, and a couple of specialized functions.

exit $?

# Compare this script to letter-count.sh.
